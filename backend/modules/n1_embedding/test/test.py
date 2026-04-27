from __future__ import annotations

import json
from typing import Any, Dict
from pathlib import Path

import sys
import os

# ─────────────────────────────────────────────
# FIX IMPORT PATH (ONLY FOR MODULE IMPORTS)
# ─────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from n1_embedding import embed


# ─────────────────────────────────────────────
# OUTPUT DIRECTORY SETUP
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR
OUTPUT_DIR.mkdir(exist_ok=True)


# ─────────────────────────────────────────────
# SAVE JSON (None-safe + stable path)
# ─────────────────────────────────────────────
def save_json(result: dict, filename: str):
    def sanitize(obj: Any):
        if isinstance(obj, dict):
            return {k: sanitize(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [sanitize(v) for v in obj]
        return obj

    payload = sanitize(result)

    output_path = OUTPUT_DIR / filename

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"[saved] {output_path}")


# ─────────────────────────────────────────────
# USER TEST
# ─────────────────────────────────────────────
def test_user():
    data: Dict[str, Any] = {
        "text": "Tôi muốn một chuyến đi yên tĩnh gần thiên nhiên",
        "image_description": None,
        "tags": ["thiên nhiên", "yên tĩnh", "couple"],
    }

    result = embed(data)
    save_json(result, "user_embedding.json")


# ─────────────────────────────────────────────
# LOCATION TEST
# ─────────────────────────────────────────────
def test_location():
    data: Dict[str, Any] = {
        "text": "Busy coastal city with nightlife and beaches",
        "tags": ["beach", "city", "nightlife"],
    }

    result = embed(data)
    save_json(result, "location_embedding.json")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("Running USER test...")
    test_user()

    print("Running LOCATION test...")
    test_location()