from __future__ import annotations

import json
from typing import Any, Dict

from . import embed


# ─────────────────────────────────────────────
# Pretty print (NONE SAFE)
# ─────────────────────────────────────────────
def pretty_print(result: dict):
    print("\n════════ EMBED RESULT ════════")

    print("Type:", result["type"])

    vectors = result["vectors"]

    for name, vec in vectors.items():

        # IMPORTANT: handle missing channel
        if vec is None:
            print(f"\n[{name}] None (no signal)")
            continue

        print(f"\n[{name}] dim={len(vec)}")
        print("head:", vec[:5])

    print("\n══════════════════════════════\n")


# ─────────────────────────────────────────────
# Save JSON (None-safe)
# ─────────────────────────────────────────────
def save_json(result: dict, filename: str):
    def sanitize(obj: Any):
        if isinstance(obj, dict):
            return {k: sanitize(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [sanitize(v) for v in obj]
        if obj is None:
            return None
        return obj

    payload = sanitize(result)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────
# USER TEST
# ─────────────────────────────────────────────
def test_user():
    data: Dict[str, Any] = {
        "text": "Tôi muốn một chuyến đi yên tĩnh gần thiên nhiên",
        "image_description": "",
        "tags": ["thiên nhiên", "yên tĩnh", "couple"],
    }

    result = embed(data)

    pretty_print(result)
    save_json(result, "user_embedding.json")


# ─────────────────────────────────────────────
# LOCATION TEST
# ─────────────────────────────────────────────
def test_location():
    data: Dict[str, Any] = {
        "description": "Busy coastal city with nightlife and beaches",
        "tags": ["beach", "city", "nightlife"],
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