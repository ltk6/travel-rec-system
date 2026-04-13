# =============================================================================
# n5_llm_generator.py
# Module hỗ trợ sinh hoạt động du lịch bằng LLM (Large Language Model).
#
# === HYBRID APPROACH - LÝ DO CHỌN ===
# Việc xây dựng database template thủ công (rule-based) có nhiều hạn chế:
#   1. Tốn thời gian xây dựng và bảo trì dữ liệu cho từng địa điểm.
#   2. Không thể bao quát hết mọi sở thích cá nhân của người dùng.
#   3. Hoạt động gợi ý bị giới hạn bởi số lượng template có sẵn.
#
# Hybrid approach kết hợp LLM giúp:
#   - Giảm công sức xây dựng data thủ công: LLM có thể sinh ra hoạt động
#     cho bất kỳ địa điểm nào, ngay cả khi chưa có template.
#   - Tăng tính cá nhân hóa: LLM hiểu context sở thích, ngân sách, thời gian
#     của người dùng để đề xuất hoạt động phù hợp hơn.
#   - Fallback an toàn: Khi LLM không khả dụng (mất mạng, hết API key, lỗi),
#     hệ thống tự động chuyển về rule-based để đảm bảo luôn có kết quả.
# =============================================================================

import json
import os
import re
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


# ===========================================================================
# CẤU HÌNH LLM
# API key được đọc từ biến môi trường GEMINI_API_KEY.
# Nếu không có key → tự động fallback về rule-based.
# ===========================================================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"


def _is_llm_available() -> bool:
    """Kiểm tra xem có thể sử dụng LLM hay không (có API key hợp lệ)."""
    return bool(GEMINI_API_KEY and GEMINI_API_KEY.strip())


def _build_prompt(
    location_name: str,
    location_description: str,
    user_tags: List[str],
    budget: int,
    duration: int,
) -> str:
    """
    Xây dựng prompt chất lượng cao cho LLM.

    Prompt được thiết kế theo nguyên tắc:
      - Rõ ràng về vai trò (role): chuyên gia du lịch Việt Nam
      - Cung cấp đầy đủ context: địa điểm, sở thích, ràng buộc
      - Yêu cầu output format JSON chuẩn, dễ parse
      - Chỉ dẫn cụ thể về nội dung: thực tế, phù hợp Việt Nam
      - Ràng buộc số lượng: 4-6 hoạt động
    """
    tags_str = ", ".join(user_tags) if user_tags else "không có sở thích cụ thể"
    budget_str = f"{budget:,}".replace(",", ".")
    
    prompt = f"""Bạn là một chuyên gia du lịch Việt Nam giàu kinh nghiệm. Hãy gợi ý các hoạt động du lịch dựa trên thông tin sau:

📍 Địa điểm: {location_name}
📝 Mô tả địa điểm: {location_description}
❤️ Sở thích của du khách: {tags_str}
💰 Ngân sách tối đa cho hoạt động: {budget_str} VNĐ
⏰ Thời gian tối đa mỗi hoạt động: {duration} phút

YÊU CẦU:
1. Sinh ra từ 4 đến 6 hoạt động cụ thể, thực tế, có thể thực hiện tại {location_name}.
2. Mỗi hoạt động PHẢI có các trường sau:
   - "name": tên hoạt động (tiếng Việt, ngắn gọn)
   - "desc": mô tả ngắn 1-2 câu
   - "cost": chi phí ước tính bằng VNĐ (số nguyên, 0 nếu miễn phí)
   - "time": thời gian ước tính (phút, số nguyên)
   - "tags": danh sách 1-3 từ khóa phân loại (tiếng Anh, ví dụ: "nature", "food", "culture", "adventure", "relax", "photography", "history", "sports", "shopping", "entertainment", "health", "education", "sea", "beach", "fun", "music", "family", "sightseeing")

3. Chi phí PHẢI nằm trong ngân sách {budget_str} VNĐ.
4. Thời gian PHẢI không vượt quá {duration} phút.
5. Ưu tiên hoạt động phù hợp với sở thích: {tags_str}.
6. Hoạt động phải thực tế và khả thi tại Việt Nam, phản ánh đúng đặc trưng địa phương.
7. Đa dạng loại hoạt động (không trùng lặp).

TRẢ LỜI BẰNG JSON THUẦN TÚY (không markdown, không giải thích thêm):
[
  {{"name": "...", "desc": "...", "cost": 0, "time": 0, "tags": ["..."]}}
]"""
    return prompt


def _parse_llm_response(response_text: str) -> Optional[List[Dict]]:
    """
    Parse phản hồi từ LLM thành danh sách hoạt động.
    
    Xử lý nhiều trường hợp:
      - JSON thuần túy
      - JSON nằm trong markdown code block (```json ... ```)
      - JSON lẫn với text thừa
    
    Returns None nếu không parse được.
    """
    if not response_text or not response_text.strip():
        logger.warning("LLM trả về response rỗng")
        return None
    
    text = response_text.strip()
    
    # Trường hợp 1: Thử parse trực tiếp
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        pass
    
    # Trường hợp 2: Tìm JSON trong markdown code block ```json ... ```
    code_block_pattern = r'```(?:json)?\s*\n?(.*?)\n?\s*```'
    matches = re.findall(code_block_pattern, text, re.DOTALL)
    for match in matches:
        try:
            data = json.loads(match.strip())
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            continue
    
    # Trường hợp 3: Tìm mảng JSON đầu tiên trong text
    bracket_start = text.find('[')
    bracket_end = text.rfind(']')
    if bracket_start != -1 and bracket_end != -1 and bracket_end > bracket_start:
        try:
            data = json.loads(text[bracket_start:bracket_end + 1])
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass
    
    logger.warning(f"Không thể parse LLM response: {text[:200]}...")
    return None


def _validate_activity(act: Dict) -> bool:
    """
    Kiểm tra một activity từ LLM có đủ các trường bắt buộc và hợp lệ không.
    
    Đảm bảo dữ liệu từ LLM tuân thủ schema trước khi đưa vào pipeline.
    """
    required_fields = ["name", "desc", "cost", "time", "tags"]
    
    # Kiểm tra đủ trường
    for field in required_fields:
        if field not in act:
            logger.warning(f"Activity thiếu trường '{field}': {act}")
            return False
    
    # Kiểm tra kiểu dữ liệu
    if not isinstance(act["name"], str) or not act["name"].strip():
        return False
    if not isinstance(act["desc"], str):
        return False
    if not isinstance(act["tags"], list):
        return False
    
    # Chuẩn hóa cost và time về số nguyên
    try:
        act["cost"] = int(act["cost"])
        act["time"] = int(act["time"])
    except (ValueError, TypeError):
        return False
    
    # Cost và time phải không âm
    if act["cost"] < 0 or act["time"] <= 0:
        return False
    
    return True


def call_gemini_api(prompt: str) -> Optional[str]:
    """
    Gọi Gemini API để sinh nội dung từ prompt.
    
    Sử dụng urllib thay vì requests để giảm phụ thuộc bên ngoài.
    Trả về text response hoặc None nếu có lỗi.
    """
    if not _is_llm_available():
        logger.info("Không có GEMINI_API_KEY, bỏ qua LLM")
        return None
    
    import urllib.request
    import urllib.error
    
    url = f"{GEMINI_API_URL}/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,       # Đủ sáng tạo nhưng không quá ngẫu nhiên
            "topP": 0.9,
            "maxOutputTokens": 2048,   # Đủ cho 4-6 activities dạng JSON
        }
    }
    
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        
        # Trích xuất text từ Gemini response format
        candidates = result.get("candidates", [])
        if candidates:
            content = candidates[0].get("content", {})
            parts = content.get("parts", [])
            if parts:
                return parts[0].get("text", "")
        
        logger.warning(f"Gemini trả về format không mong đợi: {result}")
        return None
        
    except urllib.error.HTTPError as e:
        logger.error(f"Gemini API HTTP error {e.code}: {e.reason}")
        return None
    except urllib.error.URLError as e:
        logger.error(f"Gemini API connection error: {e.reason}")
        return None
    except Exception as e:
        logger.error(f"Gemini API unexpected error: {e}")
        return None


def generate_activities_from_llm(
    location_name: str,
    location_description: str,
    user_tags: List[str],
    budget: int,
    max_time_per_activity: int,
) -> Optional[List[Dict]]:
    """
    Sinh hoạt động du lịch bằng LLM (Gemini API).
    
    Quy trình:
      1. Xây dựng prompt từ context người dùng
      2. Gọi Gemini API
      3. Parse JSON response
      4. Validate từng activity
      5. Trả về danh sách đã validate
    
    Returns:
        List[Dict] nếu thành công, None nếu thất bại (sẽ fallback rule-based).
    """
    if not _is_llm_available():
        return None
    
    # Bước 1: Xây dựng prompt
    prompt = _build_prompt(
        location_name=location_name,
        location_description=location_description,
        user_tags=user_tags,
        budget=budget,
        duration=max_time_per_activity,
    )
    
    # Bước 2: Gọi LLM
    logger.info(f"Gọi Gemini API cho địa điểm: {location_name}")
    response_text = call_gemini_api(prompt)
    
    if response_text is None:
        logger.warning(f"Gemini API không trả về kết quả cho {location_name}")
        return None
    
    # Bước 3: Parse response
    activities = _parse_llm_response(response_text)
    
    if activities is None:
        logger.warning(f"Không parse được response cho {location_name}")
        return None
    
    # Bước 4: Validate và lọc
    valid_activities = []
    for act in activities:
        if _validate_activity(act):
            # Chuẩn hóa tags thành lowercase
            act["tags"] = [tag.lower().strip() for tag in act["tags"]]
            valid_activities.append(act)
        else:
            logger.warning(f"Activity không hợp lệ bị bỏ qua: {act}")
    
    if not valid_activities:
        logger.warning(f"Không có activity hợp lệ từ LLM cho {location_name}")
        return None
    
    logger.info(f"LLM sinh thành công {len(valid_activities)} hoạt động cho {location_name}")
    return valid_activities
