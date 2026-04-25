"""
rank_locations.py
=================
N4 — Location Ranking Module

Ranks locations by computing weighted cosine similarity between
user vectors (from N1) and location vectors (from DB/N3).

Scoring weights:
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

# ── Scoring weights ───────────────────────────────────────────
WEIGHTS = {
    "emotion": 0.3,
    "context": 0.2,
    "tag":     0.4,
    "image":   0.1,
}


# ── Helpers ───────────────────────────────────────────────────

def _dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def _norm(v: list[float]) -> float:
    return math.sqrt(sum(x * x for x in v))


def _cosine(a: list[float] | None, b: list[float] | None) -> float:
    """Return cosine similarity in [−1, 1], or 0.0 if either vector is None/empty."""
    if not a or not b:
        return 0.0
    na, nb = _norm(a), _norm(b)
    if na == 0.0 or nb == 0.0:
        return 0.0
    return _dot(a, b) / (na * nb)


def _score_location(
    user_vectors: dict[str, Any],
    loc_vectors: dict[str, Any],
) -> tuple[float, str]:
    """
    Compute the weighted similarity score for one location.

    user_vectors keys expected  : emotion, context, image, tag
    loc_vectors  keys expected  : text, tag

    Returns (score: float, reason: str).
    """
    user_emotion = user_vectors.get("emotion")
    user_context = user_vectors.get("context")
    user_image   = user_vectors.get("image")
    user_tag     = user_vectors.get("tag")

    loc_text = loc_vectors.get("text")
    loc_tag  = loc_vectors.get("tag")

    # ── similarities ─────────────────────────────
    sim_emotion = _cosine(user_emotion, loc_text)
    sim_context = _cosine(user_context, loc_text)
    sim_image   = _cosine(user_image, loc_text)
    sim_tag     = _cosine(user_tag, loc_tag)

    # ── weighted sum ─────────────────────────────────────────
    score = (
        WEIGHTS["emotion"] * sim_emotion
        + WEIGHTS["context"] * sim_context
        + WEIGHTS["tag"]    * sim_tag
        + WEIGHTS["image"]  * sim_image
    )

    # ── human-readable reason ────────────────────────────────
    parts: list[str] = []
    if sim_emotion >= 0.3:
        parts.append(f"cảm xúc phù hợp ({sim_emotion:.2f})")
    if sim_context >= 0.3:
        parts.append(f"hoàn cảnh phù hợp ({sim_context:.2f})")
    if sim_tag >= 0.3:
        parts.append(f"sở thích khớp ({sim_tag:.2f})")
    if sim_image >= 0.3:
        parts.append(f"hình ảnh tương đồng ({sim_image:.2f})")
    reason = " · ".join(parts) if parts else "Địa điểm phổ biến"

    return round(float(score), 4), reason


def rank_locations(data: dict) -> dict:
    """
    N4 — Location Ranking

    Input:
    {
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
                }
            }
        ],
        "top_k": int
    }

    Output:
    {
        "locations": [
            {
                "location_id": str,
                "score":       float,
                "reason":      str
            }
        ]
    }
    """
    
    user_vectors = data.get("user_vectors", {})
    locations    = data.get("locations", [])
    top_k        = int(data.get("top_k", 5))

    if not locations:
        logger.warning("[N4] Không có địa điểm nào để xếp hạng")
        return {"locations": []}

    scored: list[dict] = []
    for loc in locations:
        loc_id       = loc.get("location_id", "unknown")
        loc_vectors  = loc.get("location_vectors", {})

        try:
            score, reason = _score_location(user_vectors, loc_vectors)
        except Exception as exc:
            logger.warning(f"[N4] Lỗi tính điểm cho {loc_id}: {exc}")
            score, reason = 0.0, "Lỗi tính điểm"

        scored.append({
            "location_id": loc_id,
            "score":       score,
            "reason":      reason,
        })

    # Sort descending by score
    scored.sort(key=lambda x: x["score"], reverse=True)
    result = scored[:top_k]

    logger.info(f"[N4] Đã xếp hạng {len(locations)} địa điểm → top {len(result)}")
    return {"locations": result}