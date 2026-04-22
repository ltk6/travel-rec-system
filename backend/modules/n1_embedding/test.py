from __future__ import annotations

import json
from datetime import datetime

from n1_embedding import embed


# ─────────────────────────────────────────────
# Pretty print
# ─────────────────────────────────────────────
def pretty_print(result: dict):
    print("\n════════ EMBED RESULT ════════")

    print("Type:", result["type"])

    vectors = result["vectors"]

    for name, vec in vectors.items():
        print(f"\n[{name}] dim={len(vec)}")
        print("head:", vec[:5])

    print("\n══════════════════════════════\n")


# ─────────────────────────────────────────────
# Save JSON
# ─────────────────────────────────────────────
def save_json(result: dict, filename: str):
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "data": result
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────
# USER TEST (ONE INPUT ONLY)
# ─────────────────────────────────────────────
def test_user():
    data = {
        "text": "Tôi muốn một chuyến đi yên tĩnh gần thiên nhiên",
        "image_description": "Peaceful misty highland with wooden cabin",
        "tags": ["thiên nhiên", "yên tĩnh", "couple"]
    }

    result = embed(data)

    pretty_print(result)
    save_json(result, "user_embedding.json")


# ─────────────────────────────────────────────
# LOCATION TEST
# ─────────────────────────────────────────────
def test_location():
    data = {
        "description": "Busy coastal city with nightlife and beaches",
        "tags": ["beach", "city", "nightlife"]
    }

    result = embed(data)

    pretty_print(result)
    save_json(result, "location_embedding.json")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("Running USER test...")
    test_user()

    print("Running LOCATION test...")
    test_location()