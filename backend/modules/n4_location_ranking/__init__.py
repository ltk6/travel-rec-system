"""
─────────────────────────────────────────────
N4 — LOCATION RANKING MODULE
─────────────────────────────────────────────

Ranks travel locations using weighted cosine similarity between
user vectors (from N1) and location vectors (from N3).

Weights are computed dynamically based on user_input richness.
Constraint soft penalties are applied when budget/duration are provided.

─────────────────────────────────────────────
INPUT
─────────────────────────────────────────────
{
    "user_input": {                          # optional — enables dynamic weights
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
                "text": list[float] | None,
                "tag":  list[float] | None
            },

            "metadata": {                    # used for constraint penalty
                "price_level":        int   | None,  # VNĐ, integer
                "estimated_duration": int   | None,  # giờ, integer
                "name":               str | None,
                "description":        str | None,
                "tags":               list[str] | None
            },

            "geo": {                         # received but not used in scoring
                "lat": float | None,
                "lng": float | None
            }
        }
    ],

    "constraints": {                         # optional — triggers soft penalty
        "budget":   float | None,           # VNĐ — so sánh với price_level
        "duration": float | None,           # giờ — so sánh với estimated_duration
        "people":   int   | None            # chưa dùng, reserved
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
            "score":       float,           # [0.0, 1.0], đã áp penalty nếu có
            "reason":      str              # giải thích tiếng Việt
        }
    ]
}

─────────────────────────────────────────────
CHƯA IMPLEMENT (planned)
─────────────────────────────────────────────
- geo proximity scoring (context.user_location lat/lng)
- constraints.people penalty
- hard filtering (loại hẳn địa điểm vượt budget)
"""

from .rank_locations import rank_locations

__all__ = ["rank_locations"]
