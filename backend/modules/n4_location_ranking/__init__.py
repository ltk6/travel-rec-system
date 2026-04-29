"""
─────────────────────────────────────────────
N4 — LOCATION RANKING MODULE (MULTI-SIGNAL SCORING ENGINE)
─────────────────────────────────────────────

This module ranks travel locations using precomputed embeddings
and structured constraints.

It combines:
- User vectors from N1 (text/aug_text/aug_tags/img_desc)
- Location embeddings (text/tag)
- sig_k-based dynamic channel weighting

─────────────────────────────────────────────
INPUT
─────────────────────────────────────────────
{
    "sig_k": int,

    "user_vectors": {
        "text":     list[float] | None,
        "aug_text": list[float] | None,
        "aug_tags": list[float] | None,
        "img_desc": list[float] | None
    },

    "locations": [
        {
            "location_id": str,

            "geo": {
                "lat": float | None,
                "lng": float | None
            },

            "location_vectors": {
                "text": list[float] | None,
                "tag": list[float] | None
            },

            "metadata": {
                "name": str | None,
                "description": str | None,
                "tags": list[str] | None,
                "price_level": float | None,
                "estimated_duration": float | None
            }
        }
    ],

    "constraints": {
        "budget": float | None,
        "duration": float | None,
        "people": int | None
    },

    "top_k": int
}

─────────────────────────────────────────────
OUTPUT
─────────────────────────────────────────────
{
    "locations": [
        {
            "location_id": str,
            "score": float,
            "reason": str
        }
    ]
}
"""

from .rank_locations import rank_locations

__all__ = ["rank_locations"]