"""
demo.py
=======
Hardcoded demo for N1 module.

Run:
    python demo.py              (from inside n1_module/)
    python -m n1_module.demo    (from parent directory)
"""

from __future__ import annotations
import json
import sys
import os

os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

_here   = os.path.dirname(os.path.abspath(__file__))
_parent = os.path.dirname(_here)
if _parent not in sys.path:
    sys.path.insert(0, _parent)

from n1_embedding import *
from n1_embedding.maps import *


# ─────────────────────────────────────────────────────────────
# HARDCODED INPUTS  (as received from N8)
# ─────────────────────────────────────────────────────────────

SAMPLES = [
    {
        "label": "Couple — peaceful nature + culture",
        "data": {
            "text": (
                "Tôi muốn một chuyến đi yên tĩnh, gần thiên nhiên, "
                "có thể khám phá văn hóa địa phương. "
                "Tôi đang cảm thấy căng thẳng và muốn thư giãn."
            ),
            "image_description": (
                "Natural landscape / countryside. "
                "Low-rise traditional wooden structures. "
                "Peaceful, misty, quiet, green surroundings."
            ),
            "tags": ["thiên nhiên", "văn hóa", "yên tĩnh", "cặp đôi", "check-in"],
        },
    },
    {
        "label": "Solo — adventure off the beaten path",
        "data": {
            "text": (
                "I'm bored and want something completely new. "
                "Looking for an adventure, maybe off the beaten path. "
                "Love hiking and camping under the stars."
            ),
            "image_description": (
                "Mountain wilderness trail. "
                "No structures, raw dramatic nature. "
                "Wild, vast, remote atmosphere."
            ),
            "tags": ["núi", "cắm trại", "leo núi", "adventure", "stargazing"],
        },
    },
    {
        "label": "Family — beach weekend with kids",
        "data": {
            "text": (
                "Gia đình tôi muốn đi chơi cuối tuần, có trẻ nhỏ "
                "nên cần nơi an toàn. Các bé thích biển và trò chơi. "
                "Không muốn đi xa."
            ),
            "image_description": (
                "Shallow tropical beach with calm water. "
                "Colorful beach resort with slides and pool. "
                "Sunny, cheerful, safe family atmosphere."
            ),
            "tags": ["biển", "gia đình có trẻ em", "vui vẻ", "resort"],
        },
    },
]


# ─────────────────────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────────────────────

def run():
    print("=" * 64)
    print("  N1 – TEXT EMBEDDING MODULE  |  Demo")
    print("=" * 64)
    print(map_stats())

    records = []

    for i, sample in enumerate(SAMPLES, 1):
        data  = sample["data"]
        label = sample["label"]

        print(f"\n{'─' * 64}")
        print(f"  Sample {i}: {label}")
        print(f"{'─' * 64}")
        print(f"  text  : {data['text'][:80]}...")
        print(f"  tags  : {data['tags']}")

        # ── Call the module's public function
        result = embed(data)
        vector = result["vector"]

        # ── Show what the maps matched
        text_matches = scan_text(data["text"]) + scan_text(data["image_description"])
        tag_matches  = expand_tags(data["tags"])

        print(f"\n  Signals detected:")
        for m in text_matches:
            print(f"    [{m.source}] '{m.key}' → '{m.expansion[:55]}...'")
        print(f"  Tag expansions:")
        for m in tag_matches:
            translated = m.source == "tag"
            mark = "✓" if translated else "~"
            print(f"    {mark} '{m.key}' → '{m.expansion[:55]}'")

        print(f"\n  Output vector: dim={len(vector)}, "
              f"sample={[round(v, 4) for v in vector[:5]]}")

        records.append({
            "label":  label,
            "input":  data,
            "output": {"vector": vector},
        })

    # ── Console summary
    print(f"\n{'=' * 64}")
    print("  VECTOR SUMMARY")
    print(f"{'=' * 64}")
    for r in records:
        v = r["output"]["vector"]
        print(f"  {r['label']}")
        print(f"    dim={len(v)}  "
              f"first_5={[round(x, 4) for x in v[:5]]}  "
              f"last_3={[round(x, 4) for x in v[-3:]]}")

    # ── JSON output
    output_path = os.path.join(_here, "test", "n1_output.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"module": "N1", "model": "BAAI/bge-m3", "samples": records},
                  f, ensure_ascii=False, indent=2)
    print(f"\n[Output] JSON saved → {output_path}")
    print("=" * 64)


if __name__ == "__main__":
    run()