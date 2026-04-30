"""
seed_with_vectors.py
────────────────────
Seeds the database using the pre-computed vectors stored in locations_with_vectors.json.
"""

import sys
import json
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.n3_database.db_manager import init_db, save_location

def seed_database():
    json_path = CURRENT_DIR / "locations_with_vectors.json"
    
    if not json_path.exists():
        print(f"❌ Error: {json_path} not found. Run embed_locations.py first.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        locations = json.load(f)

    init_db()
    print(f"🚀 Seeding {len(locations)} locations...")
    
    for i, loc in enumerate(locations, 1):
        res = save_location(loc)
        if res.get("status") == "success":
            print(f"  [{i:02d}] Seeded: {loc['metadata']['name']}")
        else:
            print(f"  [{i:02d}] ❌ Failed: {loc['location_id']} - {res.get('message')}")
            
    print("\n✨ Database seeding complete.")

if __name__ == "__main__":
    seed_database()
