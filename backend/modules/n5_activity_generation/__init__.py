"""
─────────────────────────────────────────────
N5 — ACTIVITY GENERATION MODULE
─────────────────────────────────────────────

─────────────────────────────────────────────
INPUT
─────────────────────────────────────────────
{
    "user": {
        "text": str | None,
        "img_desc": str | None,
        "tags": list[str] | None
    },

    "locations": [
        {
            "location_id": str,
            "metadata": {
                "name": str | None,
                "description": str | None,
                "tags": list[str] | None
            }
        }
    ],

    "constraints": {
        "budget": float | None,
        "duration": float | None,
        "people": int | None,
        "time_of_day": str | None
    }
}

─────────────────────────────────────────────
OUTPUT
─────────────────────────────────────────────
{
    "activities": [
        {
            "activity_id": str,
            "location_id": str,

            "metadata": {

                # ─────────────────────────────
                # CORE IDENTITY
                # ─────────────────────────────
                "name": str,
                "description": str,

                # ─────────────────────────────
                # SEMANTIC CLASSIFICATION
                # ─────────────────────────────
                "activity_type": str,
                # adventure / relaxation / food / culture / nightlife / nature / shopping

                "activity_subtype": str | None,
                # e.g. hiking / snorkeling / street food / museum visit

                # ─────────────────────────────
                # EXPERIENCE DYNAMICS
                # ─────────────────────────────
                "intensity": float,
                # 0.0 (very chill) → 1.0 (very active)

                "physical_level": float | None,
                # effort / movement intensity indicator

                "social_level": float | None,
                # solo → group-oriented activity scale

                # ─────────────────────────────
                # CONSTRAINT FIT
                # ─────────────────────────────
                "estimated_duration": float,
                # minutes

                "price_level": float,
                # normalized cost scale

                "indoor_outdoor": str,
                # indoor / outdoor / mixed

                "weather_dependent": bool,

                # ─────────────────────────────
                # CONTEXT FIT SIGNALS
                # ─────────────────────────────
                "time_of_day_suitable": str | None
                # morning / afternoon / night / anytime
            }
        }
    ]
}
"""

from .n5_activity_generator import generate_activities
 
__all__ = ["generate_activities"]
 