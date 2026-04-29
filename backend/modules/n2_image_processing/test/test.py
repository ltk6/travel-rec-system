from __future__ import annotations

import json
from typing import Any
from pathlib import Path
import sys

# ─────────────────────────────────────────────
# SAFE IMPORT PATH
# ─────────────────────────────────────────────
CURRENT = Path(__file__).resolve()

for parent in CURRENT.parents:
    if (parent / "backend").exists():
        REPO_ROOT = parent
        break
else:
    raise RuntimeError("Could not locate repo root (missing 'backend' folder)")

sys.path.insert(0, str(REPO_ROOT))

from backend.modules.n2_image_processing import process_image


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
# IMAGE TO BYTES
# ─────────────────────────────────────────────
def image_to_bytes(path: str) -> bytes:
    return Path(path).read_bytes()


# ─────────────────────────────────────────────
# TEST DATA
# ─────────────────────────────────────────────
TEST_SET = [
    {"image": image_to_bytes(Path(__file__).parent / "city.png"), "name": "image_3"},
]

# ─────────────────────────────────────────────
# RUNNER
# ─────────────────────────────────────────────
def run_tests():
    for t in TEST_SET:
        result = process_image({"image": t["image"]})
        save_json(result, f"image_{t['name']}.json")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("Running N2 IMAGE tests...")
    run_tests()