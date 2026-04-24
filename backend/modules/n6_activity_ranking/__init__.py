"""
─────────────────────────────────────────────
N6 — ACTIVITY RANKING MODULE (MULTI-SIGNAL SCORING ENGINE)
─────────────────────────────────────────────

This module ranks generated activities (from N5) using precomputed
embeddings and structured metadata constraints.

PURPOSE:
- Rank candidate activities based on user intent and context
- Combine semantic similarity + constraint satisfaction
- Return top-k most relevant activities per user query

IMPORTANT:
- NO embedding generation
- NO activity creation
- ONLY scoring + ranking logic

─────────────────────────────────────────────
INPUT
─────────────────────────────────────────────
{
    # ───────── USER INPUT ─────────
    "user_input": {
        "text": str | None,
        "image_description": str | None,
        "tags": list[str] | None
    },

    # ───────── USER VECTORS ─────────
    "user_vectors": {
        "emotion": list[float] | None,
        "context": list[float] | None,
        "image": list[float] | None,
        "tag": list[float] | None
    },

    # ───────── CONTEXT ─────────
    "context": {
        "user_location": {
            "lat": float | None,
            "lng": float | None
        },
        "time_of_day": str | None
    },

    # ───────── ACTIVITIES ─────────
    "activities": [
        {
            "activity_id": str,
            "location_id": str,

            "metadata": {
                "name": str,
                "description": str,

                "activity_type": str,
                "activity_subtype": str | None,

                "intensity": float,
                "physical_level": float | None,
                "social_level": float | None,

                "estimated_duration": float,
                "price_level": float,

                "indoor_outdoor": str,
                "weather_dependent": bool,

                "time_of_day_suitable": str | None
            },

            "vectors": {
                "text": list[float] | None,
                "tag": list[float] | None,
                "intent": list[float] | None
            }
        }
    ],

    # ───────── CONSTRAINTS ─────────
    "constraints": {
        "budget": float | None,
        "duration": float | None,
        "people": int | None,
        "weather": str | None
    },

    "top_k": int
}

─────────────────────────────────────────────
OUTPUT
─────────────────────────────────────────────
{
    "activities": [
        {
            "activity_id": str,
            "location_id": str,
            "score": float,
            "reason": str
        }
    ]
}

─────────────────────────────────────────────
SCORING DESIGN (HIGH LEVEL)
─────────────────────────────────────────────
Semantic Matching:
- user_vectors ↔ activity_vectors (text/tag/intent)
- weighted cosine similarity fusion

Constraint Scoring:
- budget fit penalty / boost
- duration fit alignment
- group size compatibility (if applicable)

Context Scoring:
- time_of_day match
- weather_dependency alignment
- indoor/outdoor preference alignment

Geographic influence (optional):
- derived from location layer (if propagated)

─────────────────────────────────────────────
DESIGN PRINCIPLES
─────────────────────────────────────────────
- Fully deterministic scoring
- Missing vectors must be safely ignored (no failure propagation)
- No generation or embedding logic
- Explainable output via reason field
- Shared scoring architecture with N4 but activity-specialized signals
─────────────────────────────────────────────
"""

def rank_activities(data: dict) -> dict:
    pass

__all__ = ["rank_activities"]