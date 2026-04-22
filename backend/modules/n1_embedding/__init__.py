"""
n1_module
=========

Unified embedding API for user and location inputs.

Each input is processed independently through a structured semantic pipeline:
→ registry expansion (emotion / context / tags / image)
→ channel-wise enriched representation
→ multi-vector embedding using a shared model

This ensures consistent semantic representation across user queries
and location documents for retrieval and ranking.

Public API
----------

    from n1_embedding import embed

    result = embed({
        "text": "Tôi muốn một chuyến đi yên tĩnh gần thiên nhiên",
        "image_description": "Peaceful misty highland, wooden structures",
        "tags": ["thiên nhiên", "yên tĩnh", "couple"]
    })

    print(result["type"])                 # "user" | "location"
    print(result["vectors"]["context"])   # list[float], 1024-dim
"""

from __future__ import annotations

from typing import Dict, Any, List

from .embedder import embed_texts
from .preprocessor import build_user_input, build_location_input
from .maps import stats as map_stats


def embed(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Unified embedding API (SINGLE INPUT ONLY)

    Input:
        USER:
        {
            "text": str,
            "image_description": str,
            "tags": list[str]
        }

        LOCATION:
        {
            "description": str,
            "tags": list[str]
        }

    Output:
        {
            "type": "user" | "location",
            "vectors": {
                "expanded_emotion": [...],
                "expanded_context": [...],
                "expanded_tag": [...],
                "expanded_image": [...]
            }
        }
    """

    if not isinstance(data, dict):
        raise ValueError("embed() now only accepts a single dict")

    # ─────────────────────────────────────────────
    # 1. detect type
    # ─────────────────────────────────────────────
    is_location = "description" in data

    if is_location:
        processed = build_location_input(
            description=data.get("description", ""),
            tags=data.get("tags", []),
        )
        input_type = "location"
    else:
        processed = build_user_input(
            text=data.get("text", ""),
            image_description=data.get("image_description", ""),
            tags=data.get("tags", []),
        )
        input_type = "user"

    # ─────────────────────────────────────────────
    # 2. embed each semantic channel
    # ─────────────────────────────────────────────
    keys = list(processed.keys())
    texts = [processed[k] for k in keys]

    vectors = embed_texts(texts)

    # ─────────────────────────────────────────────
    # 3. return clean structure (NO IDs)
    # ─────────────────────────────────────────────
    return {
        "type": input_type,
        "vectors": dict(zip(keys, vectors))
    }


__all__ = ["embed", "map_stats"]