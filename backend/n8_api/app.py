"""
n8_api/app.py
=============
N8 – API Orchestrator (Flask)

Pipeline:
N2 (image → img_desc) → N1 (embed) → N3 (db) → N4 (rank locations)

Contract summary:
─────────────────────────────────────────────
N2 input:  { image: bytes }
N2 output: { img_desc: str }

N1 input:  { text, tags, img_desc }
N1 output: { sig_k, preprocessed, vectors: { text, aug_text, aug_tags, img_desc } }

N3 output: { status, total, data: [{ location_id, vectors: { text, aug_text, aug_tags, image_description }, metadata, geo }] }

N4 input:  { sig_k, user_vectors: { text, aug_text, aug_tags, img_desc }, locations: [{ location_id, location_vectors: { text, tag } }], top_k }
N4 output: { locations: [{ location_id, score, reason }] }
─────────────────────────────────────────────
"""

from __future__ import annotations

import sys
import os
import logging
import base64
from typing import Any

from flask import Flask, request, jsonify
from flask_cors import CORS

# ── Path setup ────────────────────────────────────────────────
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

# ── Database ──────────────────────────────────────────────────
from n3_database import get_all_locations

# ── Modules ───────────────────────────────────────────────────
from modules.n1_embedding import embed
from modules.n2_image_processing import process_image
from modules.n4_location_ranking import rank_locations
from modules.n4_location_ranking.rank_locations import _get_weights

# ── Logging ───────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("N8")

# ── App ───────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)


# ═════════════════════════════════════════════════════════════
# HELPERS
# ═════════════════════════════════════════════════════════════

def _err(msg: str, code: int = 400):
    return jsonify({"error": msg}), code


def _get_json():
    data = request.get_json(silent=True)
    if not data:
        return None, _err("Invalid JSON body")
    return data, None


def _safe_vec(v):
    """Ensure value is a Python list. Handles numpy arrays from pgvector."""
    if v is None:
        return []
    if isinstance(v, list):
        return v
    # numpy arrays from pgvector
    if hasattr(v, 'tolist'):
        return v.tolist()
    try:
        return list(v)
    except (TypeError, ValueError):
        return []


# ═════════════════════════════════════════════════════════════
# HEALTH
# ═════════════════════════════════════════════════════════════

@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "pipeline": ["n1", "n2", "n3", "n4"]
    })


# ═════════════════════════════════════════════════════════════
# FULL PIPELINE
# ═════════════════════════════════════════════════════════════

@app.post("/recommend")
def recommend():
    body, err = _get_json()
    if err:
        return err

    text = body.get("text", "").strip()
    image_b64 = body.get("image", "")
    tags = body.get("tags", [])
    constraints = body.get("constraints", {})
    top_k = int(body.get("top_k_locations", 5))

    if not text and not tags:
        return _err("Provide text or tags")

    # ── N2 — Image → img_desc ──────────────────
    img_desc = ""
    if image_b64:
        try:
            img_bytes = base64.b64decode(image_b64)
            n2_result = process_image({"image": img_bytes})
            img_desc = n2_result.get("img_desc", "")
        except Exception as e:
            logger.warning(f"N2 failed: {e}")

    # ── N1 — Embed user input ──────────────────
    # N1 contract: { text, tags, img_desc } → { sig_k, preprocessed, vectors }
    n1_result = embed({
        "text": text,
        "tags": tags,
        "img_desc": img_desc,
    })

    sig_k = n1_result.get("sig_k", 0)
    vectors = n1_result.get("vectors", {})

    # User vectors: text, aug_text, aug_tags, img_desc
    user_vectors = {
        "text":     _safe_vec(vectors.get("text")),
        "aug_text": _safe_vec(vectors.get("aug_text")),
        "aug_tags": _safe_vec(vectors.get("aug_tags")),
        "img_desc": _safe_vec(vectors.get("img_desc")),
    }

    # ── N3 — Fetch locations from DB ───────────
    # N3 returns { status, total, data: [...] }
    db_result = get_all_locations()
    locations = db_result.get("data", []) if isinstance(db_result, dict) else []

    # ── Build N4 input ─────────────────────────
    # N4 expects location_vectors: { text, tag }
    # N3 DB stores: text, aug_text, aug_tags, image_description
    # Mapping: N3.text → N4.text, N3.aug_tags → N4.tag
    n4_locations = []
    loc_map = {}

    for loc in locations:
        loc_id = loc.get("location_id", "unknown")
        db_vectors = loc.get("vectors", {}) or {}

        n4_locations.append({
            "location_id": loc_id,
            "location_vectors": {
                "text": _safe_vec(db_vectors.get("text")),
                "tag":  _safe_vec(db_vectors.get("aug_tags")),
            }
        })

        loc_map[loc_id] = {
            "vectors": db_vectors,
            "metadata": loc.get("metadata", {}),
            "geo": loc.get("geo", {}),
            "image_path": loc.get("image_path", ""),
        }

    # ── N4 — Rank locations ────────────────────
    # N4 contract: { sig_k, user_vectors, locations, top_k }
    n4_result = rank_locations({
        "sig_k": sig_k,
        "user_vectors": user_vectors,
        "locations": n4_locations,
        "top_k": top_k,
    })

    ranked = n4_result.get("locations", [])

    return jsonify({
        # ─────────────────────────────
        # MAIN CONTRACT (DO NOT CHANGE)
        # ─────────────────────────────
        "locations": [
            {
                "location_id": r["location_id"],
                "score": r.get("score", 0),
                "reason": r.get("reason", ""),

                "metadata": loc_map.get(r["location_id"], {}).get("metadata", {}),
                "geo": loc_map.get(r["location_id"], {}).get("geo", {}),
                "image_path": loc_map.get(r["location_id"], {}).get("image_path", ""),
            }
            for r in ranked
        ],

        # ─────────────────────────────
        # FULL TRACE (EVERYTHING)
        # ─────────────────────────────
        "trace": {
            # ─── USER SIDE ───
            "user": {
                "input": {
                    "text": text,
                    "tags": tags,
                    "constraints": constraints,
                    "has_image": bool(image_b64),
                },
                "n2_image": {
                    "img_desc": img_desc,
                },
                "n1_embedding": {
                    "sig_k": sig_k,
                    "preprocessed": n1_result.get("preprocessed", {}),
                },
                "user_vectors": user_vectors,
                "vector_dims": {
                    k: len(v) if v else 0
                    for k, v in user_vectors.items()
                },
            },

            # ─── LOCATION SIDE (RAW BEFORE RANKING) ───
            "locations_raw": [
                {
                    "location_id": loc.get("location_id"),
                    "metadata": loc.get("metadata", {}),
                    "geo": loc.get("geo", {}),
                }
                for loc in locations
            ],

            # ─── RANKING OUTPUT ───
            "ranking": {
                "sig_k": sig_k,
                "weights_used": _get_weights(sig_k),
                "top_k": top_k,
                "ranked": ranked,
            },

            # ─── SYSTEM DEBUG ───
            "debug": {
                "total_locations": len(n4_locations),
                "pipeline": {
                    "n1": "embedding",
                    "n2": "image_processing",
                    "n3": "database_fetch",
                    "n4": "ranking",
                },
            },
        },
    })

# ═════════════════════════════════════════════════════════════
# RUN
# ═════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)