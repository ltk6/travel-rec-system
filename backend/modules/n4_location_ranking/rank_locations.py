"""
rank_locations.py
=================
N4 — Location Ranking Module

Ranks locations by computing weighted cosine similarity between
user vectors (from N1) and location vectors (from DB/N3).

Weights are computed dynamically from user_input richness:
  - text length  → emotion + context signals
  - tag count    → tag signal
  - image present → image signal

Falls back to fixed WEIGHTS when user_input is absent:
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

# ── Fallback weights (when user_input is absent) ──────────────
WEIGHTS = {
    "emotion": 0.3,
    "context": 0.2,
    "tag":     0.4,
    "image":   0.1,
}

# ── Base informativeness per input type ───────────────────────
# Reflects how expressive each source is per unit of input.
# Text (natural language) > Image (specific when present) > Tag (predefined).
SIGNAL_BASE = {
    "text":  1.0,
    "tag":   0.5,
    "image": 0.9,
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


# ── Dynamic weight helpers ────────────────────────────────────

def _presence_text(word_count: int) -> float:
    """
    Presence factor for text input.
    Floor of 0.5 ensures even very short text has meaningful weight —
    natural language is more expressive than predefined tags regardless of length.
    Saturates at 30 words.
    """
    if word_count == 0:
        return 0.0
    return max(0.5, min(1.0, word_count / 30.0))


def _presence_tag(tag_count: int) -> float:
    """Linear presence factor for tags. 10 tags = full confidence."""
    return min(1.0, tag_count / 10.0)


def _compute_weights(
    user_input: dict[str, Any],
    user_vectors: dict[str, Any],
) -> dict[str, float]:
    """
    Compute dynamic scoring weights based on user input richness.

    Three principles:
    1. Absent input -> weight zeroed out (no guessing from empty vectors).
    2. Text has a base advantage: presence floor 0.5 even when very short.
    3. All four weights normalize to sum = 1.0.

    Falls back to WEIGHTS if every signal is zero.
    """
    text       = (user_input.get("text") or "").strip()
    tags       = user_input.get("tags") or []
    image_desc = (user_input.get("image_description") or "").strip()

    word_count = len(text.split()) if text else 0
    tag_count  = len(tags) if isinstance(tags, list) else 0

    p_text  = _presence_text(word_count)
    p_tag   = _presence_tag(tag_count)
    p_image = 1.0 if image_desc else 0.0

    # Zero out if the corresponding vector is missing or empty (N1 could not embed it).
    # `not v` is True for both None and [] — intentional: both mean "no usable vector".
    if not user_vectors.get("emotion") and not user_vectors.get("context"):
        p_text = 0.0
    if not user_vectors.get("tag"):
        p_tag = 0.0
    if not user_vectors.get("image"):
        p_image = 0.0

    raw_text  = SIGNAL_BASE["text"]  * p_text
    raw_tag   = SIGNAL_BASE["tag"]   * p_tag
    raw_image = SIGNAL_BASE["image"] * p_image

    total = raw_text + raw_tag + raw_image

    if total < 1e-9:
        logger.warning("[N4] Tất cả tín hiệu đầu vào đều rỗng — dùng trọng số cố định")
        return WEIGHTS.copy()

    w_text  = raw_text  / total
    w_tag   = raw_tag   / total
    w_image = raw_image / total

    weights = {
        "emotion": round(w_text * 0.6, 4),
        "context": round(w_text * 0.4, 4),
        "tag":     round(w_tag,        4),
        "image":   round(w_image,      4),
    }

    logger.info(
        "[N4] Dynamic weights | "
        "emotion=%.3f  context=%.3f  tag=%.3f  image=%.3f | "
        "text_words=%d  tags=%d  has_image=%s",
        weights["emotion"], weights["context"], weights["tag"], weights["image"],
        word_count, tag_count, bool(image_desc),
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
        "user_input": {                      # optional — enables dynamic weights
            "text":              str | None,
            "image_description": str | None,
            "tags":              list[str] | None
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
    user_input   = data.get("user_input", {})
    user_vectors = data.get("user_vectors", {})
    locations    = data.get("locations", [])
    constraints  = data.get("constraints") or {}
    top_k        = max(1, int(data.get("top_k", 5)))

    if not locations:
        logger.warning("[N4] Không có địa điểm nào để xếp hạng")
        return {"locations": []}

    if user_input:
        weights = _compute_weights(user_input, user_vectors)
    else:
        weights = WEIGHTS
        logger.info("[N4] user_input vắng mặt — dùng trọng số cố định")

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
