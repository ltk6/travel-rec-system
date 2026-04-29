from __future__ import annotations

import json
from typing import Any, Dict
from pathlib import Path
import sys

# ─────────────────────────────────────────────
# SAFE IMPORT PATH (dynamic project root)
# ─────────────────────────────────────────────
CURRENT = Path(__file__).resolve()

for parent in CURRENT.parents:
    if (parent / "n1_embedding").exists():
        sys.path.insert(0, str(parent))
        break
else:
    raise RuntimeError("Could not locate project root containing 'n1_embedding'")

from n1_embedding import embed


# ─────────────────────────────────────────────
# OUTPUT DIRECTORY
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR
OUTPUT_DIR.mkdir(exist_ok=True)


# ─────────────────────────────────────────────
# JSON SAVE
# ─────────────────────────────────────────────
def save_json(result: dict, filename: str):
    def sanitize(obj: Any):
        if isinstance(obj, dict):
            return {k: sanitize(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [sanitize(v) for v in obj]
        return obj

    output_path = OUTPUT_DIR / filename

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(sanitize(result), f, ensure_ascii=False, indent=2)

    print(f"[saved] {output_path}")


# ─────────────────────────────────────────────
# TEST DATA
# ─────────────────────────────────────────────

USER_TESTS = [
    {
        "text": "Tôi muốn một chuyến đi yên tĩnh gần thiên nhiên",
        "tags": ["thiên nhiên", "yên tĩnh", "couple"],
        "img_desc": "A couple walking slowly on a quiet beach during sunset, warm golden light reflecting on the water, relaxed and intimate atmosphere",
        "name": "user_1"
    },
    {
        "text": "Muốn đi du lịch chữa lành tâm trí sau thời gian stress",
        "tags": ["healing", "relax", "nature"],
        "img_desc": "A person sitting quietly by a misty lake at sunrise, surrounded by mountains and soft fog, conveying calmness, healing, and emotional reset",
        "name": "user_2"
    },
    {
        "text": "Đi chơi cuối tuần nhẹ nhàng với người yêu",
        "tags": ["couple", "weekend", "romantic"],
        "img_desc": "",
        "name": "user_3"
    },
]

LOCATION_TESTS = [
    {
        "text": "Busy coastal city with nightlife and beaches",
        "tags": ["beach", "city", "nightlife"],
        "img_desc": "",
        "name": "loc_1"
    },
    {
        "text": "Quiet mountain town surrounded by forests and mist",
        "tags": ["mountain", "forest", "quiet"],
        "img_desc": "",
        "name": "loc_2"
    },
    {
        "text": "Historic city with temples, culture, and street food",
        "tags": ["culture", "history", "food"],
        "img_desc": "",
        "name": "loc_3"
    },
]


# ─────────────────────────────────────────────
# RUNNER
# ─────────────────────────────────────────────
def run_tests(test_set: list[dict], prefix: str):
    for t in test_set:
        result = embed({
            "text": t.get("text"),
            "tags": t.get("tags"),
            "img_desc": t.get("img_desc"),
        })

        save_json(result, f"{prefix}_{t['name']}.json")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("Running USER tests...")
    run_tests(USER_TESTS, "user")

    print("Running LOCATION tests...")
    run_tests(LOCATION_TESTS, "location")