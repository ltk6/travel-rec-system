"""
─────────────────────────────────────────────
N4 — LOCATION RANKING MODULE (MULTI-SIGNAL SCORING ENGINE)
─────────────────────────────────────────────

This module ranks travel locations using precomputed embeddings
and structured constraints.

It combines:
- User semantic intent (text, image, tags)
- User vector representations (emotion/context/image/tag)
- Location embeddings (text/tag)
- Contextual signals (geo proximity, budget, duration constraints)

─────────────────────────────────────────────
INPUT
─────────────────────────────────────────────
{
    "user_input": {
        "text": str | None,
        "image_description": str | None,
        "tags": list[str] | None
    },

    "user_vectors": {
        "emotion": list[float] | None,
        "context": list[float] | None,
        "image": list[float] | None,
        "tag": list[float] | None
    },

    "context": {
        "user_location": {
            "lat": float | None,
            "lng": float | None
        }
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