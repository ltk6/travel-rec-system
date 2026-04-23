from __future__ import annotations

from typing import Dict, Any

from .embedder import embed_texts
from .preprocessor import build_user_input, build_location_input
from .maps import stats as map_stats


def embed(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Unified embedding API

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

    OUTPUT:
        USER:
        {
            "type": "user",
            "vectors": {
                "emotion": [...],
                "context": [...],
                "tag": [...],
                "image": [...]
            }
        }

        LOCATION:
        {
            "type": "location",
            "vectors": {
                "text": [...],
                "tag": [...]
            }
        }
    """

    if not isinstance(data, dict):
        raise ValueError("embed() accepts a single dict only")

    # ─────────────────────────────────────────────
    # 1. detect type
    # ─────────────────────────────────────────────
    is_location = "description" in data

    # ─────────────────────────────────────────────
    # 2. USER PIPELINE
    # ─────────────────────────────────────────────
    if not is_location:
        processed = build_user_input(
            text=data.get("text", ""),
            image_description=data.get("image_description", ""),
            tags=data.get("tags", []),
        )

        # EXACT keys from preprocessor
        texts = [
            processed["expanded_emotion"],
            processed["expanded_context"],
            processed["expanded_tag"],
            processed["expanded_image"],
        ]
        vectors = embed_texts(texts)

        return {
            "type": "user",
            "vectors": {
                "emotion": vectors[0],
                "context": vectors[1],
                "tag": vectors[2],
                "image": vectors[3],
            }
        }

    # ─────────────────────────────────────────────
    # 3. LOCATION PIPELINE
    # ─────────────────────────────────────────────
    processed = build_location_input(
        description=data.get("description", ""),
        tags=data.get("tags", []),
    )

    texts = [
        processed["expanded_text"],
        processed["expanded_tag"],
    ]

    vectors = embed_texts(texts)

    return {
        "type": "location",
        "vectors": {
            "text": vectors[0],
            "tag": vectors[1],
        }
    }


__all__ = ["embed", "map_stats"]