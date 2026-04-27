"""
rank_locations.py
=================
N4 — Location Ranking Module

Ranks locations by computing weighted cosine similarity between
user vectors (from N1) and location vectors (from DB/N3).

Weights are computed dynamically from preprocessed user channels:
    - emotion keyword string length
    - context keyword string length
    - tag keyword string length
    - image keyword string length

Falls back to fixed WEIGHTS when preprocessed_user_input is absent:
    emotion  (user) vs text (location) : 0.3
    context  (user) vs text (location) : 0.2
    tag      (user) vs tag  (location) : 0.4
    image    (user) vs text (location) : 0.1
"""

from __future__ import annotations

import logging
import math
from typing import Any

logger = logging.getLogger(__name__)

# ── Fallback weights (when preprocessed_user_input is absent) ──
WEIGHTS = {
    "emotion": 0.3,
    "context": 0.2,
    "tag":     0.4,
    "image":   0.1,
}

# ── Vector helpers ────────────────────────────────────────────

def _dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def _norm(v: list[float]) -> float:
    return math.sqrt(sum(x * x for x in v))


def _cosine(a: list[float] | None, b: list[float] | None) -> float:
    """Return cosine similarity in [-1, 1], or 0.0 if either vector is None/empty."""
    if not a or not b:
        return 0.0
    if len(a) != len(b):
        logger.warning(f"[N4] Vector length mismatch: {len(a)} vs {len(b)}")
        return 0.0
    na, nb = _norm(a), _norm(b)
    if na == 0.0 or nb == 0.0:
        return 0.0
    return _dot(a, b) / (na * nb)


def _compute_weights(
    preprocessed_user_input: dict[str, Any],
    user_vectors: dict[str, Any],
) -> dict[str, float]:
    """
    Compute dynamic scoring weights based on preprocessed user channels.

    Three principles:
    1. Channel richness is measured by keyword count of each preprocessed string.
    2. Missing/empty vector channel -> its weight is forced to zero.
    3. All four weights normalize to sum = 1.0.

    Falls back to WEIGHTS if every signal is zero.
    """
    emotion_text = str(preprocessed_user_input.get("emotion") or "").strip()
    context_text = str(preprocessed_user_input.get("context") or "").strip()
    tag_text = str(preprocessed_user_input.get("tag") or "").strip()
    image_text = str(preprocessed_user_input.get("image") or "").strip()

    emotion_count = len(emotion_text.split()) if emotion_text else 0
    context_count = len(context_text.split()) if context_text else 0
    tag_count = len(tag_text.split()) if tag_text else 0
    image_count = len(image_text.split()) if image_text else 0

    raw_emotion = float(emotion_count)
    raw_context = float(context_count)
    raw_tag = float(tag_count)
    raw_image = float(image_count)

    # Zero out if the corresponding vector is missing or empty (N1 could not embed it).
    # `not v` is True for both None and [] — intentional: both mean "no usable vector".
    if not user_vectors.get("emotion"):
        raw_emotion = 0.0
    if not user_vectors.get("context"):
        raw_context = 0.0
    if not user_vectors.get("tag"):
        raw_tag = 0.0
    if not user_vectors.get("image"):
        raw_image = 0.0

    total = raw_emotion + raw_context + raw_tag + raw_image

    if total < 1e-9:
        logger.warning("[N4] Tất cả tín hiệu đầu vào đều rỗng — dùng trọng số cố định")
        return WEIGHTS.copy()

    weights = {
        "emotion": round(raw_emotion / total, 4),
        "context": round(raw_context / total, 4),
        "tag": round(raw_tag / total, 4),
        "image": round(raw_image / total, 4),
    }

    logger.info(
        "[N4] Dynamic weights | "
        "emotion=%.3f  context=%.3f  tag=%.3f  image=%.3f | "
        "emotion_kw=%d  context_kw=%d  tag_kw=%d  image_kw=%d",
        weights["emotion"], weights["context"], weights["tag"], weights["image"],
        emotion_count, context_count, tag_count, image_count,
    )
    return weights


# ── Scoring ───────────────────────────────────────────────────

def _constraint_penalty(
    metadata: dict[str, Any],
    constraints: dict[str, Any],
) -> tuple[float, list[str]]:
    """
    Compute a soft penalty multiplier in (0, 1] when location exceeds constraints.
    Returns (multiplier, penalty_notes).
    Soft (not hard filter): over-budget locations are penalised, not removed.
    """
    multiplier = 1.0
    notes: list[str] = []

    budget = constraints.get("budget")
    price_level = metadata.get("price_level")
    if budget and price_level and price_level > budget:
        multiplier *= 0.6
        notes.append(f"vượt ngân sách ({int(price_level):,} > {int(budget):,} VNĐ)")

    duration = constraints.get("duration")
    estimated = metadata.get("estimated_duration")
    if duration and estimated and estimated > duration:
        multiplier *= 0.7
        notes.append(f"vượt thời gian ({int(estimated)}h > {int(duration)}h)")

    return multiplier, notes


def _score_location(
    user_vectors: dict[str, Any],
    loc_vectors: dict[str, Any],
    weights: dict[str, float] | None = None,
    metadata: dict[str, Any] | None = None,
    constraints: dict[str, Any] | None = None,
) -> tuple[float, str]:
    """
    Compute the weighted similarity score for one location.

    user_vectors keys: emotion, context, image, tag
    loc_vectors  keys: text, tag

    Returns (score: float, reason: str).
    """
    if weights is None:
        weights = WEIGHTS

    user_emotion = user_vectors.get("emotion")
    user_context = user_vectors.get("context")
    user_image   = user_vectors.get("image")
    user_tag     = user_vectors.get("tag")

    loc_text = loc_vectors.get("text")
    loc_tag  = loc_vectors.get("tag")

    sim_emotion = _cosine(user_emotion, loc_text)
    sim_context = _cosine(user_context, loc_text)
    sim_image   = _cosine(user_image,   loc_text)
    sim_tag     = _cosine(user_tag,     loc_tag)

    score = (
        weights["emotion"] * sim_emotion
        + weights["context"] * sim_context
        + weights["tag"]     * sim_tag
        + weights["image"]   * sim_image
    )
    score = max(0.0, min(1.0, score))

    # Apply constraint soft penalty when metadata and constraints are provided
    penalty_notes: list[str] = []
    if metadata and constraints:
        penalty, penalty_notes = _constraint_penalty(metadata, constraints)
        score = round(score * penalty, 4)

    # Build reason from signals that are active (weight > 0) and match well (sim >= 0.3)
    parts: list[str] = []
    if weights["emotion"] > 0 and sim_emotion >= 0.3:
        parts.append(f"cảm xúc phù hợp ({sim_emotion:.2f})")
    if weights["context"] > 0 and sim_context >= 0.3:
        parts.append(f"hoàn cảnh phù hợp ({sim_context:.2f})")
    if weights["tag"]     > 0 and sim_tag     >= 0.3:
        parts.append(f"sở thích khớp ({sim_tag:.2f})")
    if weights["image"]   > 0 and sim_image   >= 0.3:
        parts.append(f"hình ảnh tương đồng ({sim_image:.2f})")

    if not parts:
        candidates = {
            "cảm xúc":   (sim_emotion, weights["emotion"]),
            "sở thích":  (sim_tag,     weights["tag"]),
            "hoàn cảnh": (sim_context, weights["context"]),
            "hình ảnh":  (sim_image,   weights["image"]),
        }
        best_label, (best_sim, best_w) = max(
            candidates.items(), key=lambda kv: kv[1][0] * kv[1][1]
        )
        if best_sim > 0 and best_w > 0:
            reason = f"Gợi ý chung — {best_label} ({best_sim:.2f})"
        else:
            reason = "Không đủ thông tin để xếp hạng"
    else:
        reason = " · ".join(parts)

    if penalty_notes:
        reason += " ⚠ " + ", ".join(penalty_notes)

    return round(float(score), 4), reason


# ── Public API ────────────────────────────────────────────────

def rank_locations(data: dict) -> dict:
    """
    N4 — Location Ranking

    Input:
    {
        "preprocessed_user_input": {         # optional — enables dynamic weights
            "emotion": str | None,
            "context": str | None,
            "tag":     str | None,
            "image":   str | None
        },
        "user_vectors": {
            "emotion": list[float] | None,
            "context": list[float] | None,
            "image":   list[float] | None,
            "tag":     list[float] | None
        },
        "locations": [
            {
                "location_id": str,
                "location_vectors": {
                    "text": list[float],
                    "tag":  list[float]
                },
                "metadata": {                # optional — enables constraint penalty
                    "price_level":        int | None,  # VNĐ
                    "estimated_duration": int | None   # giờ
                },
                "geo": {}                    # received, not used in scoring
            }
        ],
        "constraints": {                     # optional — triggers soft penalty
            "budget":   float | None,
            "duration": float | None,
            "people":   int   | None
        },
        "top_k": int
    }

    Output:
    {
        "locations": [
            {
                "location_id": str,
                "score":       float,        # [0.0, 1.0], đã áp penalty nếu có
                "reason":      str
            }
        ]
    }
    """
    preprocessed_user_input = (
        data.get("preprocessed_user_input")
        or data.get("user_processed_input")
        or {}
    )
    user_vectors = data.get("user_vectors", {})
    locations    = data.get("locations", [])
    constraints  = data.get("constraints") or {}
    top_k        = max(1, int(data.get("top_k", 5)))

    if not locations:
        logger.warning("[N4] Không có địa điểm nào để xếp hạng")
        return {"locations": []}

    if preprocessed_user_input:
        weights = _compute_weights(preprocessed_user_input, user_vectors)
    else:
        weights = WEIGHTS
        logger.info("[N4] preprocessed_user_input vắng mặt — dùng trọng số cố định")

    scored: list[dict] = []
    for loc in locations:
        loc_id      = loc.get("location_id", "unknown")
        loc_vectors = loc.get("location_vectors", {})
        metadata    = loc.get("metadata", {})

        try:
            score, reason = _score_location(
                user_vectors, loc_vectors, weights,
                metadata=metadata,
                constraints=constraints,
            )
        except Exception as exc:
            logger.warning("[N4] Lỗi tính điểm cho %s: %s", loc_id, exc)
            score, reason = 0.0, "Lỗi tính điểm"

        scored.append({
            "location_id": loc_id,
            "score":       score,
            "reason":      reason,
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    result = scored[:top_k]

    logger.info("[N4] Đã xếp hạng %d địa điểm → top %d", len(locations), len(result))
    return {"locations": result}
