"""
─────────────────────────────────────────────
N3 — DATABASE LAYER
─────────────────────────────────────────────

SAVE LOCATION:
Input:
{
    "location_id": str,

    "vectors": {
        "text": str,
        "aug_text": str,
        "aug_tags": str,
        "img_desc": str
    },

    "metadata": dict,
    "geo": dict
}

Output:
{
    "status": "success" | "error",
    "message": str (optional on error)
}

GET ALL LOCATIONS:
Output:
[
    {
        "location_id": str,

        "vectors": {
            "text": str,
            "aug_text": str,
            "aug_tags": str,
            "img_desc": str
        },

        "metadata": dict,
        "geo": dict
    }
]
"""

from .db_manager import (
    init_db,
    save_user_profile,
    save_location,
    get_all_locations,
)