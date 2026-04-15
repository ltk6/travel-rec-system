"""
N8 — API Orchestrator (Bộ Điều Phối Trung Tâm)
================================================
Endpoint chính: POST /api/v1/recommend

Pipeline:
    N7 → N8 → [N2 HTTP] → N1 → N3 → N4 → N5 → N6 → N7

Nguyên tắc thiết kế:
    - N2 là service riêng (FastAPI/uvicorn) → N8 gọi qua HTTP.
    - N1, N3, N5, N6 là Python module → N8 import trực tiếp.
    - N4 chưa có code → dùng stub, tự động thay khi N4 sẵn sàng.
    - Mỗi bước đều có error handling riêng.
    - N2 lỗi/timeout → graceful fallback (bỏ qua ảnh, tiếp tục với text).
    - N3 offline → trả về lỗi 503 rõ ràng.
    - N1 lỗi vector rỗng → trả về lỗi 422 rõ ràng.
"""

import os
import sys
import uuid
import time
import logging
from datetime import datetime, timezone
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ─────────────────────────────────────────────────────────────────────────────
# Thêm project root vào sys.path để import các module backend
# ─────────────────────────────────────────────────────────────────────────────
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ─────────────────────────────────────────────────────────────────────────────
# Import các module nội bộ (N1, N3, N5, N6)
# ─────────────────────────────────────────────────────────────────────────────
from backend.modules.n1_embedding import embed  # noqa: E402
from backend.modules.n3_database.db_manager import (  # noqa: E402
    save_user_profile,
    filter_locations,
    get_all_locations,
)
from backend.modules.n5_activity_generation.n5_activity_generator import (  # noqa: E402
    generate_activities_hybrid,
)
from backend.modules.n6_activity_ranking.rank_activities import rank_activities  # noqa: E402

# ─────────────────────────────────────────────────────────────────────────────
# N4: Thử import — nếu chưa có code thì dùng stub tự động
# ─────────────────────────────────────────────────────────────────────────────
N4_AVAILABLE = False
try:
    from backend.modules.n4_location_ranking.rank_locations import rank_locations  # noqa: E402
    N4_AVAILABLE = True
except ImportError:
    pass  # Sẽ dùng stub _stub_rank_locations bên dưới

# ─────────────────────────────────────────────────────────────────────────────
# Cấu hình Logging & Biến môi trường
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger("N8")

# URL của N2 service (FastAPI chạy riêng bằng uvicorn)
N2_SERVICE_URL = os.getenv("N2_SERVICE_URL", "http://localhost:8001/api/v1/process-image")
N2_TIMEOUT_SECONDS = float(os.getenv("N2_TIMEOUT", "10"))


# ═════════════════════════════════════════════════════════════════════════════
# FastAPI App
# ═════════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="N8 — Smart Tourism API Orchestrator",
    description=(
        "Điều phối toàn bộ pipeline N1→N6, "
        "trả kết quả gợi ý hành trình du lịch cá nhân hóa cho N7."
    ),
    version="1.0.0",
)

# CORS: cho phép N7 (frontend) gọi từ bất kỳ origin nào (chế độ dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═════════════════════════════════════════════════════════════════════════════
# PYDANTIC SCHEMAS — Định nghĩa Input / Output
# ═════════════════════════════════════════════════════════════════════════════

class Preferences(BaseModel):
    """Sở thích và mong muốn của người dùng."""
    text: str = Field(
        default="",
        description="Yêu cầu văn bản tự do (vi/en/mixed)",
        examples=["Tôi muốn đi nơi yên tĩnh, nhiều cây xanh"],
    )
    image_url: str | None = Field(
        default=None,
        description="URL ảnh minh họa trải nghiệm mong muốn (tuỳ chọn)",
        examples=["https://example.com/forest.jpg"],
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Tag sở thích từ bài trắc nghiệm",
        examples=[["nature", "relax", "couple"]],
    )


class Constraints(BaseModel):
    """Ràng buộc thực tế của chuyến đi."""
    budget: float = Field(
        default=5_000_000,
        ge=0,
        description="Tổng ngân sách (VNĐ)",
    )
    duration: int = Field(
        default=24,
        ge=1,
        description="Tổng thời gian chuyến đi (giờ)",
    )
    people: int = Field(
        default=1,
        ge=1,
        description="Số người tham gia",
    )


class RecommendRequest(BaseModel):
    """
    Schema nhận từ N7.
    Theo MVP instructions: { text, image_url, tags, constraints }
    """
    user_id: str | None = Field(
        default=None,
        description="UUID người dùng nếu đã đăng nhập (tuỳ chọn)",
    )
    preferences: Preferences = Field(default_factory=Preferences)
    constraints: Constraints = Field(default_factory=Constraints)

    model_config = {
        "json_schema_extra": {
            "example": {
                "preferences": {
                    "text": "Tôi muốn đi nơi yên tĩnh, nhiều thiên nhiên",
                    "image_url": "https://example.com/nature.jpg",
                    "tags": ["nature", "relax", "trekking"],
                },
                "constraints": {
                    "budget": 3000000,
                    "duration": 48,
                    "people": 2,
                },
            }
        }
    }


# ═════════════════════════════════════════════════════════════════════════════
# STUB N4 — Placeholder khi N4 chưa có code
# ═════════════════════════════════════════════════════════════════════════════

def _stub_rank_locations(
    vector: list[float],
    locations: list[dict],
    constraints: dict,
    top_k: int,
) -> dict:
    """
    Placeholder cho N4 khi module chưa được implement.

    Hành vi: Trả về tất cả locations với score mặc định 1.0.
    Khi N4 có code thật, xóa stub này và uncomment import ở trên.

    Input/Output giữ đúng spec MVP:
        Output: { "locations": [{ "location_id": "...", "score": 1.0 }] }
    """
    logger.warning(
        "⚠️  N4 chưa có code — dùng stub. "
        "Tất cả locations được giữ lại với score=1.0."
    )
    return {
        "locations": [
            {
                "location_id": loc.get(
                    "location_id",
                    loc.get("metadata", {}).get("name", "unknown"),
                ),
                "score": 1.0,
            }
            for loc in locations[:top_k]
        ]
    }


# ═════════════════════════════════════════════════════════════════════════════
# BƯỚC 1 — N2: Image Processing (HTTP Request)
# ═════════════════════════════════════════════════════════════════════════════

async def _step1_call_n2(image_url: str | None) -> str:
    """
    Gọi N2 service qua HTTP để lấy mô tả ảnh.

    N2 chạy riêng bằng uvicorn (port 8001 mặc định).
    N8 cần fetch ảnh từ URL → gửi bytes lên N2 dưới dạng multipart/form-data.

    Graceful fallback:
        - Không có image_url      → trả ""
        - N2 timeout              → log warning, trả ""
        - N2 HTTP error           → log warning, trả ""
        - Bất kỳ lỗi nào         → log warning, trả ""
    Pipeline vẫn tiếp tục bình thường với text only.
    """
    if not image_url:
        logger.info("[B1] Không có image_url → bỏ qua N2")
        return ""

    try:
        logger.info(f"[B1] Gọi N2 với image_url: {image_url}")
        async with httpx.AsyncClient(timeout=N2_TIMEOUT_SECONDS) as client:
            # 1. Fetch ảnh từ URL
            img_resp = await client.get(image_url)
            img_resp.raise_for_status()

            # 2. Gửi bytes lên N2 (N2 nhận multipart file)
            n2_resp = await client.post(
                N2_SERVICE_URL,
                files={"file": ("image.jpg", img_resp.content, "image/jpeg")},
            )
            n2_resp.raise_for_status()

            # 3. Lấy mô tả (lưu ý: N2 code gốc có typo "image_decription")
            data = n2_resp.json()
            description = data.get("image_decription") or data.get("image_description") or ""
            logger.info(f"[B1] N2 → image_description: {description[:100]}... ✅")
            return description

    except httpx.TimeoutException:
        logger.warning("[B1] N2 timeout — fallback: bỏ qua ảnh, tiếp tục với text")
    except httpx.HTTPStatusError as exc:
        logger.warning(f"[B1] N2 HTTP {exc.response.status_code} — fallback")
    except Exception as exc:
        logger.warning(f"[B1] N2 lỗi không xác định ({exc!r}) — fallback")

    return ""


# ═════════════════════════════════════════════════════════════════════════════
# BƯỚC 2 — N1: Text Embedding (import trực tiếp)
# ═════════════════════════════════════════════════════════════════════════════

def _step2_call_n1(
    text: str,
    image_description: str,
    tags: list[str],
) -> list[float]:
    """
    Gộp text + image_description + tags → gửi vào N1 → nhận vector 1024-dim.

    N1 dùng BAAI/bge-m3 (Lazy Loading — model load lần đầu chậm).
    Nếu vector rỗng → raise HTTP 422 (Unprocessable Entity).

    Input spec (MVP):
        { "text": "...", "image_description": "...", "tags": [...] }
    Output spec:
        { "vector": [float, ...] }  # 1024 chiều
    """
    logger.info("[B2] Gọi N1 embed()...")
    result = embed({
        "text": text,
        "image_description": image_description,
        "tags": tags,
    })
    vector = result.get("vector", [])

    if not vector:
        raise HTTPException(
            status_code=422,
            detail={
                "error_code": "N1_EMBEDDING_FAILED",
                "message": (
                    "N1 không thể tạo vector embedding. "
                    "Model BAAI/bge-m3 có thể chưa được load hoặc bị lỗi."
                ),
                "step_failed": "N1",
            },
        )

    logger.info(f"[B2] N1 → vector {len(vector)}-dim ✅")
    return vector


# ═════════════════════════════════════════════════════════════════════════════
# BƯỚC 3 — N3: Database (import trực tiếp)
# ═════════════════════════════════════════════════════════════════════════════

def _step3_call_n3(
    user_id: str,
    vector: list[float],
    text: str,
    image_description: str,
    tags: list[str],
    budget: float,
    duration: int,
    people: int,
) -> tuple[list[dict], dict]:
    """
    Lưu user profile (vector + metadata + constraints) vào MongoDB.
    Truy vấn danh sách locations phù hợp với budget và duration.

    Fallback:
        - filter_locations() rỗng → dùng get_all_locations()
        - DB offline hoàn toàn → raise HTTP 503

    Trả về:
        (locations: list[dict], location_map: dict[location_id → full_loc])
    """
    logger.info("[B3] Lưu user profile vào N3...")
    save_result = save_user_profile({
        "user_id": user_id,
        "vector": vector,
        "metadata": {
            "text": text,
            "image_description": image_description,
            "tags": tags,
        },
        "constraints": {
            "budget": budget,
            "duration": duration,
            "people": people,
        },
    })
    if save_result.get("status") == "error":
        logger.warning(f"[B3] Lưu user profile thất bại: {save_result.get('message')}")

    logger.info("[B3] Truy vấn locations từ N3...")
    locations = filter_locations(budget=budget, duration=duration)

    if not locations:
        logger.warning("[B3] filter_locations() rỗng → fallback: get_all_locations()")
        locations = get_all_locations()

    if not locations:
        raise HTTPException(
            status_code=503,
            detail={
                "error_code": "N3_DB_EMPTY",
                "message": (
                    "Không có địa điểm nào trong database. "
                    "Vui lòng seed dữ liệu địa điểm trước (seed_data.py)."
                ),
                "step_failed": "N3",
            },
        )

    # Tạo lookup map: location_id → full location object
    location_map: dict[str, dict] = {}
    for loc in locations:
        loc_id = (
            loc.get("location_id")
            or loc.get("metadata", {}).get("name")
            or "unknown"
        )
        location_map[loc_id] = loc

    logger.info(f"[B3] N3 → {len(locations)} locations ✅")
    return locations, location_map


# ═════════════════════════════════════════════════════════════════════════════
# BƯỚC 4 — N4: Location Ranking (import trực tiếp / stub)
# ═════════════════════════════════════════════════════════════════════════════

def _step4_call_n4(
    vector: list[float],
    locations: list[dict],
    constraints: dict,
    top_k: int = 5,
) -> list[dict]:
    """
    Xếp hạng địa điểm theo cosine similarity giữa user vector và location vector.
    Dùng N4 thật nếu có code, ngược lại dùng stub.

    Input spec (MVP):
        vector, locations[], constraints, top_k
    Output spec:
        { "locations": [{ "location_id": "...", "score": float }] }

    Trả về:
        ranked_locations: list[dict]  — đã sắp xếp theo score giảm dần
    """
    logger.info(f"[B4] Gọi N4 rank_locations (top_k={top_k}, N4_AVAILABLE={N4_AVAILABLE})...")
    ranker = rank_locations if N4_AVAILABLE else _stub_rank_locations  # type: ignore[name-defined]
    result = ranker(
        vector=vector,
        locations=locations,
        constraints=constraints,
        top_k=top_k,
    )
    ranked = result.get("locations", [])
    logger.info(f"[B4] N4 → {len(ranked)} locations đã xếp hạng ✅")
    return ranked


# ═════════════════════════════════════════════════════════════════════════════
# BƯỚC 5 — N5: Activity Generation (import trực tiếp)
# ═════════════════════════════════════════════════════════════════════════════

def _step5_call_n5(
    tags: list[str],
    ranked_locations: list[dict],
    location_map: dict,
    budget: float,
    duration_hours: int,
) -> list[dict]:
    """
    Sinh danh sách hoạt động phù hợp cho các địa điểm đã xếp hạng.

    N5 nhận:
        user_tags: list[str]         — từ trắc nghiệm / text
        locations: list[dict]        — cần có "name" và "description"
        constraints: dict            — budget, max_time_per_day

    Lưu ý: N5 dùng tag matching (không dùng vector trực tiếp).
    Hybrid mode: thử Gemini LLM → fallback rule-based template.

    Trả về: list activities với đầy đủ metadata (name, cost, time, tags, score, reason)
    """
    logger.info(f"[B5] Gọi N5 generate_activities_hybrid ({len(ranked_locations)} locations)...")

    # Chuẩn bị input cho N5: cần "name" và "description" cho mỗi location
    n5_locations: list[dict] = []
    for item in ranked_locations:
        loc_id = item.get("location_id", "")
        full_loc = location_map.get(loc_id, {})
        meta = full_loc.get("metadata", {})
        n5_locations.append({
            "name": meta.get("name", loc_id),
            "description": meta.get("description", f"Địa điểm du lịch {loc_id} tại Việt Nam"),
            "score": item.get("score", 1.0),
        })

    # Giới hạn thời gian mỗi ngày: lấy tối đa 8 giờ/ngày hoặc nửa tổng thời gian
    max_time_per_day = min(480, duration_hours * 60 // max(1, duration_hours // 24 + 1))

    activities = generate_activities_hybrid(
        user_tags=tags,
        locations=n5_locations,
        constraints={
            "budget": budget,
            "max_time_per_day": max_time_per_day,
        },
        use_llm=True,
    )

    logger.info(f"[B5] N5 → {len(activities)} activities ✅")
    return activities


# ═════════════════════════════════════════════════════════════════════════════
# BƯỚC 6 — N6: Activity Ranking (import trực tiếp)
# ═════════════════════════════════════════════════════════════════════════════

def _step6_call_n6(
    vector: list[float],
    activities: list[dict],
    budget: float,
    duration_hours: int,
    top_k: int = 10,
) -> dict:
    """
    Xếp hạng activities theo cosine similarity với user vector.

    LƯU Ý kỹ thuật:
        N6 yêu cầu mỗi activity có trường 'embedding' hoặc 'vector'.
        N5 hiện tại không trả về embedding riêng cho activity.
        Workaround tạm thời: dùng user vector làm placeholder (điểm sẽ uniform).
        TODO: N5 cần bổ sung field 'embedding' cho mỗi activity trong tương lai.

    Input spec (MVP):
        { vector, activities[], constraints, top_k }
    Output spec:
        { "activities": [{ "activity_id", "location_id", "score", "cost", "time" }] }
    """
    logger.info(f"[B6] Gọi N6 rank_activities (top_k={top_k})...")

    # Enrich activities: thêm trường 'embedding' và 'rating' mà N6 yêu cầu
    enriched: list[dict] = []
    for act in activities:
        enriched.append({
            **act,
            # Dùng user vector làm placeholder cho activity embedding
            # (N6 tính cosine similarity giữa user_vec và act_vec)
            "embedding": act.get("embedding", act.get("vector", vector)),
            # Convert match_score (0-1) → rating (0-5) cho N6
            "rating": round(act.get("match_score", 0.5) * 5, 2),
        })

    result = rank_activities(
        vector=vector,
        activities=enriched,
        constraints={
            "max_cost": budget,
            "max_time": duration_hours * 60,  # convert giờ → phút
            "min_rating": 0.0,
        },
        top_k=top_k,
    )

    logger.info(f"[B6] N6 → {len(result.get('activities', []))} activities đã xếp hạng ✅")
    return result


# ═════════════════════════════════════════════════════════════════════════════
# BƯỚC 7 — Format Output → N7
# ═════════════════════════════════════════════════════════════════════════════

def _step7_format_output(
    request_id: str,
    ranked_locations: list[dict],
    location_map: dict,
    activities_n5: list[dict],
    activities_n6: dict,
    processing_time_ms: int,
) -> dict:
    """
    Merge kết quả từ N4 (locations + score), N5 (activity detail), N6 (activity score)
    thành JSON chuẩn trả về N7.

    Cấu trúc output (theo n8.docx):
    {
        "status": "success",
        "request_id": "...",
        "processing_time_ms": ...,
        "generated_at": "...",
        "data": {
            "recommendations": [
                {
                    "location": { "id", "name", "match_score" },
                    "itinerary": {
                        "total_cost": ...,
                        "total_duration": ...,
                        "activities": [{ "id", "name", "description", "cost",
                                         "duration", "tags", "score", "reason_summary" }]
                    }
                }
            ]
        }
    }
    """
    # Lookup nhanh: activity_id → full detail từ N5
    act_detail_map: dict[str, dict] = {
        a["activity_id"]: a for a in activities_n5
    }

    # Nhóm activities đã rank (N6) theo location_id
    loc_to_acts: dict[str, list[dict]] = {}
    for ranked_act in activities_n6.get("activities", []):
        act_id  = ranked_act.get("activity_id", "")
        loc_id  = ranked_act.get("location_id", "")
        detail  = act_detail_map.get(act_id, {})

        loc_to_acts.setdefault(loc_id, []).append({
            "id":             act_id,
            "name":           detail.get("name", act_id),
            "description":    detail.get("description", ""),
            "cost":           ranked_act.get("cost", detail.get("cost", 0)),
            "duration":       ranked_act.get("time", detail.get("estimated_time_minutes", 0)),
            "tags":           detail.get("tags", []),
            "score":          round(ranked_act.get("score", 0), 4),
            "reason_summary": detail.get("reason_summary", ""),
        })

    # Build danh sách recommendations theo thứ tự N4 đã xếp hạng
    recommendations: list[dict] = []
    for loc_item in ranked_locations:
        loc_id   = loc_item.get("location_id", "")
        full_loc = location_map.get(loc_id, {})
        meta     = full_loc.get("metadata", {})
        acts     = loc_to_acts.get(loc_id, [])

        recommendations.append({
            "location": {
                "id":          loc_id,
                "name":        meta.get("name", loc_id),
                "match_score": round(loc_item.get("score", 0), 4),
            },
            "itinerary": {
                "total_cost":     sum(a["cost"] for a in acts),
                "total_duration": sum(a["duration"] for a in acts),
                "activities":     acts,
            },
        })

    return {
        "status":             "success",
        "request_id":         request_id,
        "processing_time_ms": processing_time_ms,
        "generated_at":       datetime.now(timezone.utc).isoformat(),
        "data": {
            "recommendations": recommendations,
        },
    }


# ═════════════════════════════════════════════════════════════════════════════
# ENDPOINT CHÍNH: POST /api/v1/recommend
# ═════════════════════════════════════════════════════════════════════════════

@app.post(
    "/api/v1/recommend",
    summary="Gợi ý hành trình du lịch cá nhân hóa",
    response_description="Danh sách địa điểm và lịch trình hoạt động phù hợp với người dùng",
)
async def recommend(req: RecommendRequest) -> dict[str, Any]:
    """
    Pipeline N8 — 7 bước tuần tự:

    1. [N2] Xử lý ảnh qua HTTP → image_description
    2. [N1] Embedding văn bản → user vector 1024-dim
    3. [N3] Lưu profile + truy vấn locations từ MongoDB
    4. [N4] Xếp hạng địa điểm theo cosine similarity
    5. [N5] Sinh danh sách hoạt động (hybrid LLM + rule-based)
    6. [N6] Xếp hạng hoạt động
    7. [Format] Merge output → trả JSON chuẩn về N7
    """
    request_id = str(uuid.uuid4())
    t_start    = time.perf_counter()
    logger.info(f"{'═'*60}")
    logger.info(f"[N8] Request [{request_id}] bắt đầu")
    logger.info(f"{'═'*60}")

    # ── Unpack input ──────────────────────────────────────────────────────────
    user_id  = req.user_id or str(uuid.uuid4())
    text     = req.preferences.text.strip()
    image_url = req.preferences.image_url
    tags     = req.preferences.tags
    budget   = req.constraints.budget
    duration = req.constraints.duration
    people   = req.constraints.people
    constraints_dict = {"budget": budget, "duration": duration, "people": people}

    # ── Validate: cần ít nhất text hoặc tags ─────────────────────────────────
    if not text and not tags:
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "INVALID_INPUT",
                "message": "Cần ít nhất 'text' hoặc 'tags' để tạo gợi ý.",
                "step_failed": "INPUT_VALIDATION",
            },
        )

    # ── Bước 1: N2 — Image Processing ────────────────────────────────────────
    image_description = await _step1_call_n2(image_url)

    # ── Bước 2: N1 — Text Embedding ──────────────────────────────────────────
    vector = _step2_call_n1(text, image_description, tags)

    # ── Bước 3: N3 — Database ────────────────────────────────────────────────
    locations, location_map = _step3_call_n3(
        user_id=user_id,
        vector=vector,
        text=text,
        image_description=image_description,
        tags=tags,
        budget=budget,
        duration=duration,
        people=people,
    )

    # ── Bước 4: N4 — Location Ranking ────────────────────────────────────────
    ranked_locations = _step4_call_n4(
        vector=vector,
        locations=locations,
        constraints=constraints_dict,
        top_k=5,
    )

    # ── Bước 5: N5 — Activity Generation ─────────────────────────────────────
    activities_n5 = _step5_call_n5(
        tags=tags,
        ranked_locations=ranked_locations,
        location_map=location_map,
        budget=budget,
        duration_hours=duration,
    )

    if not activities_n5:
        logger.warning("[N8] N5 không sinh được hoạt động nào — kết quả sẽ rỗng")

    # ── Bước 6: N6 — Activity Ranking ────────────────────────────────────────
    activities_n6 = _step6_call_n6(
        vector=vector,
        activities=activities_n5,
        budget=budget,
        duration_hours=duration,
        top_k=10,
    )

    # ── Bước 7: Format Output ─────────────────────────────────────────────────
    processing_ms = int((time.perf_counter() - t_start) * 1000)
    response      = _step7_format_output(
        request_id=request_id,
        ranked_locations=ranked_locations,
        location_map=location_map,
        activities_n5=activities_n5,
        activities_n6=activities_n6,
        processing_time_ms=processing_ms,
    )

    logger.info(f"[N8] Request [{request_id}] hoàn thành trong {processing_ms}ms ✅")
    logger.info(f"{'═'*60}")
    return response


# ═════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK
# ═════════════════════════════════════════════════════════════════════════════

@app.get("/health", summary="Kiểm tra trạng thái N8")
def health_check() -> dict:
    """Trả về trạng thái hoạt động của N8 và các module phụ thuộc."""
    return {
        "status":        "ok",
        "timestamp":     datetime.now(timezone.utc).isoformat(),
        "modules": {
            "n1_embedding":  "import ✅",
            "n2_image":      f"HTTP service tại {N2_SERVICE_URL}",
            "n3_database":   "import ✅",
            "n4_ranking":    "import ✅" if N4_AVAILABLE else "stub ⚠️  (chưa có code)",
            "n5_activity":   "import ✅",
            "n6_ranking":    "import ✅",
        },
    }


# ═════════════════════════════════════════════════════════════════════════════
# CHẠY LOCAL
# Lệnh chạy: uvicorn backend.n8_api.main:app --reload --port 8000
# Swagger UI: http://localhost:8000/docs
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
