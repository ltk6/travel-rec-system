"""
embed_locations.py
==================
Embeds all locations using N1 (real BGE-M3 if available).

Outputs:
  - locations_with_vectors.json
  - seed_with_vectors.py
"""

from __future__ import annotations
import sys, os, json, time

# ── Ensure project root is on path
_here = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(_here)
if _root not in sys.path:
    sys.path.insert(0, _root)

from backend.n3_database.seed_data import LOCATIONS

# ─────────────────────────────────────────────────────────────
# LOAD N1 (REAL OR FALLBACK)
# ─────────────────────────────────────────────────────────────

try:
    from n1_embedding import embed as n1_embed
    print("[N1] Using real BGE-M3 embeddings")
    _N1_REAL = True

except ImportError as e:
    print(f"[N1] Import failed ({e}) — using SHA-256 mock")

    import hashlib, math

    def _sha_embed(text: str) -> list[float]:
        digest = hashlib.sha256(text.encode()).digest()
        raw    = [b / 255.0 for b in digest]
        tiled  = (raw * (1024 // len(raw) + 1))[:1024]
        norm   = math.sqrt(sum(x * x for x in tiled)) or 1.0
        return [x / norm for x in tiled]

    def n1_embed(data: dict) -> dict:
        text = f"{data.get('text', '')} {' '.join(data.get('tags', []))}"
        return {"vector": _sha_embed(text)}

    _N1_REAL = False


# ─────────────────────────────────────────────────────────────
# EMBED LOGIC
# ─────────────────────────────────────────────────────────────

def embed_location(loc: dict) -> list[float]:
    meta = loc["metadata"]

    enriched_text = meta["description"] + " " + " ".join(meta["tags"])

    result = n1_embed({
        "text": enriched_text,
        "image_description": "",
        "tags": meta["tags"],
    })

    return result["vector"]


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
        'from db_manager import init_db, save_location',
        '',
        'LOCATIONS = [',
    ]

    for loc in locations:
        meta = loc["metadata"]
        geo  = loc["geo"]

        lines += [
            '    {',
            f'        "location_id": {repr(loc["location_id"])},',
            f'        "vector": {repr(loc["vector"])},',
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
    print(f"Mode: {'BGE-M3 (REAL)' if _N1_REAL else 'SHA-256 (MOCK)'}")
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
            "vector": vec,
            "metadata": loc["metadata"],
            "geo": loc["geo"],
        })

    json_path = os.path.join(_here, "locations_with_vectors.json")
    py_path   = os.path.join(_here, "seed_with_vectors.py")

    _write_json(embedded, json_path)
    _write_python(embedded, py_path)

    print("\nSaved:")
    print(f" - {json_path}")
    print(f" - {py_path}")
    print(f"\nVector dim: {len(embedded[0]['vector'])}")
    print("="*60 + "\n")

    return embedded


if __name__ == "__main__":
    run()