"""
embed_locations.py
==================
Embeds all locations using N1 (real BGE-M3 if available).

Outputs:
  - locations_with_vectors.json
  - seed_with_vectors.py
"""

from __future__ import annotations
import sys, json, time
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.n3_database.seed_data import LOCATIONS
from backend.modules.n1_embedding import embed

print("[N1] Using REAL BGE-M3 embeddings")


# ─────────────────────────────────────────────────────────────
# EMBED LOGIC
# ─────────────────────────────────────────────────────────────

def embed_location(loc: dict) -> list[float]:
    meta = loc["metadata"]

    result = embed({
        "text": meta["description"],
        "tags": meta["tags"],
    })

    return result["vectors"]


# ─────────────────────────────────────────────────────────────
# WRITE OUTPUTS
# ─────────────────────────────────────────────────────────────

def _write_json(locations: list[dict], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(locations, f, ensure_ascii=False, indent=2)


def _write_python(locations: list[dict], path: str) -> None:
    lines = [
        '"""',
        'seed_with_vectors.py',
        'Auto-generated — DO NOT EDIT',
        '"""',
        '',
        'from .db_manager import init_db, save_location',
        '',
        'LOCATIONS = [',
    ]

    for loc in locations:
        meta = loc["metadata"]
        geo  = loc["geo"]
        vecs = loc["vectors"]

    for loc in locations:
        meta = loc["metadata"]
        geo  = loc["geo"]
        vecs = loc["vectors"]

        lines += [
            '    {',
            f'        "location_id": {repr(loc["location_id"])},',
            '        "vectors": {',
            f'            "text": {repr(vecs["text"])},',
            f'            "aug_text": {repr(vecs["aug_text"])},',
            f'            "aug_tags": {repr(vecs["aug_tags"])},',
            f'            "img_desc": {repr(vecs["img_desc"])},',
            '        },',
            f'        "metadata": {{',
            f'            "name": {repr(meta["name"])},',
            f'            "description": {repr(meta["description"])},',
            f'            "tags": {repr(meta["tags"])},',
            f'            "price_level": {meta["price_level"]},',
            f'            "estimated_duration": {meta["estimated_duration"]},',
            f'        }},',
            f'        "geo": {{"lat": {geo["lat"]}, "lng": {geo["lng"]}}},',
            '    },',
        ]

    lines += [
        ']',
        '',
        'def seed_database():',
        '    init_db()',
        '    print(f"Seeding {len(LOCATIONS)} locations...")',
        '    for loc in LOCATIONS:',
        '        save_location(loc)',
        '    print("Done!")',
        '',
        'if __name__ == "__main__":',
        '    seed_database()',
    ]


    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def run() -> list[dict]:
    print("\n" + "="*60)
    print(f"Embedding {len(LOCATIONS)} locations")
    print("Mode: N1 REAL (returns 4-vector dict)")
    print("="*60 + "\n")

    embedded = []

    for i, loc in enumerate(LOCATIONS, 1):
        name = loc["metadata"]["name"]

        t0  = time.time()
        vec = embed_location(loc)
        ms  = (time.time() - t0) * 1000

        print(f"[{i:02d}] {name:<35} dim={len(vec)} ({ms:.0f}ms)")

        embedded.append({
            "location_id": loc["location_id"],
            "vectors": vec,
            "metadata": loc["metadata"],
            "geo": loc["geo"],
        })

    json_path = Path(__file__).resolve().parent / "locations_with_vectors.json"
    py_path   = Path(__file__).resolve().parent / "seed_with_vectors.py"

    _write_json(embedded, json_path)
    _write_python(embedded, py_path)

    print("\nSaved:")
    print(f" - {json_path}")
    print(f" - {py_path}")
    print(f"\nVector sample dims: {len(embedded[0]['vectors']['text'])}")
    print("=" * 60 + "\n")

    return embedded


if __name__ == "__main__":
    run()