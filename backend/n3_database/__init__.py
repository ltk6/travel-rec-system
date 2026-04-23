"""
─────────────────────────────────────────────
N3 — DATABASE LAYER (POSTGRES + JSONB STORAGE)
─────────────────────────────────────────────
SAVE LOCATION:
Input:
{
    "location_id": str,
    "vectors": dict,
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
        "vectors": dict,
        "metadata": dict,
        "geo": dict
    }
]
"""

from .db_manager import (
    init_db,
    save_location, 
    get_all_locations, 
)