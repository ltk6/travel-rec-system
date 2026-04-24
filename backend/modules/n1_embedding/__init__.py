from __future__ import annotations

from typing import Dict, Any

from .embedder import embed_texts
from .preprocessor import build_user_input, build_location_input
from .maps import stats as map_stats


def embed(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Unified embedding API.

    ── USER INPUT ────────────────────────────────────────────
    {
        "text":              str,
        "image_description": str,
        "tags":              list[str]
    }

    ── LOCATION INPUT ────────────────────────────────────────
    {
        "description": str,
        "tags":        list[str]
    }

    ── USER OUTPUT ───────────────────────────────────────────
    {
        "type": "user",
        "preprocessed": {
            "emotion": str,
            "context": str,
            "tag":     str,
            "image":   str,
        },
        "vectors": {
            "emotion": [...] | None,
            "context": [...] | None,
            "tag":     [...] | None,
            "image":   [...] | None,
        }
    }

    ── LOCATION OUTPUT ───────────────────────────────────────
    {
        "type": "location",
        "vectors": {
            "text": [...] | None,
            "tag":  [...] | None,
        }
    }
    """
    if not isinstance(data, dict):
        raise ValueError("embed() accepts a single dict only")

    is_location = "description" in data

    # ── User pipeline ─────────────────────────────────────────
    if not is_location:
        preprocessed = build_user_input(
            text=data.get("text", ""),
            image_description=data.get("image_description", ""),
            tags=data.get("tags", []),
        )

        vectors = embed_texts([
            preprocessed["expanded_emotion"],
            preprocessed["expanded_context"],
            preprocessed["expanded_tag"],
            preprocessed["expanded_image"],
        ])

        return {
            "type": "user",
            "preprocessed": {
                "emotion": preprocessed["expanded_emotion"],
                "context": preprocessed["expanded_context"],
                "tag":     preprocessed["expanded_tag"],
                "image":   preprocessed["expanded_image"],
        },
            "vectors": {
                "emotion": vectors[0],
                "context": vectors[1],
                "tag":     vectors[2],
                "image":   vectors[3],
            },
        }

    # ── Location pipeline ─────────────────────────────────────
    preprocessed = build_location_input(
        description=data.get("description", ""),
        tags=data.get("tags", []),
    )

    vectors = embed_texts([
        preprocessed["expanded_text"],
        preprocessed["expanded_tag"],
    ])

    return {
        "type": "location",
        "vectors": {
            "text": vectors[0],
            "tag":  vectors[1],
        },
    }


__all__ = ["embed", "map_stats"]