"""
n8_module/app.py
================
N8 – API Orchestrator (Flask)

Pipeline:
N2 (image) → N1 (embed) → N3 (db) → N4 (rank locations)
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
    return v if isinstance(v, list) else []


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

    # ── N2 ─────────────────────────────
    if image_b64:
        try:
            img = base64.b64decode(image_b64)
            res = process_image({"image": img})
            image_desc = res.get("image_description", "")
        except Exception as e:
            logger.warning(f"N2 failed: {e}")
            image_desc = ""
    else:
        image_desc = ""

    # ── N1 ─────────────────────────────
    embed_result = embed({
        "text": text,
        "image_description": image_desc,
        "tags": tags
    })

    vectors = embed_result.get("vectors", {})

    user_vectors = {
        "emotion": _safe_vec(vectors.get("emotion")),
        "context": _safe_vec(vectors.get("context")),
        "image":   _safe_vec(vectors.get("image")),
        "tag":     _safe_vec(vectors.get("tag")),
    }

    # ── N3 ─────────────────────────────
    locations = get_all_locations()

    # ── N4 INPUT FORMAT ─────────────────────────────
    n4_locations = []
    loc_map = {}

    for loc in locations:
        loc_id = loc.get("location_id", "unknown")

        vectors = loc.get("vectors", {}) or {}

        n4_locations.append({
            "location_id": loc_id,
            "location_vectors": {
                "text": _safe_vec(vectors.get("text")),
                "tag":  _safe_vec(vectors.get("tag")),
            }
        })

        loc_map[loc_id] = {
            "vectors": vectors,
            "metadata": loc.get("metadata", {}),
            "geo": loc.get("geo", {})
        }

    # ── N4 ─────────────────────────────
    result = rank_locations({
        "user_vectors": user_vectors,
        "locations": n4_locations,
        "top_k": top_k
    })

    ranked = result.get("locations", [])

    return jsonify({
        # ─────────────────────────────
        # MAIN CONTRACT (DO NOT CHANGE)
        # ─────────────────────────────
        "locations": [
            {
                "location_id": r["location_id"],
                "score": r.get("score", 0),
                "reason": r.get("reason", ""),

                "vectors": loc_map.get(r["location_id"], {}).get("vectors", {}),
                "metadata": loc_map.get(r["location_id"], {}).get("metadata", {}),
                "geo": loc_map.get(r["location_id"], {}).get("geo", {})
            }
            for r in ranked
        ],

        # ─────────────────────────────
        # FULL TRACE (NEW — EVERYTHING)
        # ─────────────────────────────
        "trace": {
            # ─── USER SIDE ───
            "user": {
                "input": {
                    "text": text,
                    "tags": tags,
                    "constraints": constraints,
                    "has_image": bool(image_b64)
                },
                "image_processing": {
                    "image_description": image_desc
                },
                "vectors": user_vectors,
                "vector_dims": {
                    k: len(v) if v is not None else 0
                    for k, v in user_vectors.items()
                }
            },

            # ─── LOCATION SIDE (RAW BEFORE RANKING) ───
            "locations_raw": [
                {
                    "location_id": loc.get("location_id"),
                    "vectors": loc.get("vectors", {}),
                    "metadata": loc.get("metadata", {}),
                    "geo": loc.get("geo", {})
                }
                for loc in locations
            ],

            # ─── RANKING OUTPUT ───
            "ranking": {
                "top_k": top_k,
                "ranked": ranked
            },

            # ─── SYSTEM DEBUG ───
            "debug": {
                "total_locations": len(n4_locations),
                "pipeline": {
                    "n1": "embedding",
                    "n2": "image_processing",
                    "n3": "database_fetch",
                    "n4": "ranking"
                }
            }
        }
    })

# ═════════════════════════════════════════════════════════════
# RUN
# ═════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)