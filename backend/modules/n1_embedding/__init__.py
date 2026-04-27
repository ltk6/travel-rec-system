from __future__ import annotations

from typing import Dict, Any

from .embedder import embed_texts
from .preprocessor import build_inputs
from .maps import stats as map_stats


def embed(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Unified embedding API.

    ── INPUT ────────────────────────────────────────────
    {
        "text":              str | None,
        "tags":              list[str] | None,
        "image_description": str | None,
    }

    ── OUTPUT ───────────────────────────────────────────
    {
        "preprocessed": {
            "text":               str,
            "aug_text":           str,
            "aug_tags":           str,
            "image_description":  str
        },
        "vectors": {
            "text":               [...] | None,
            "aug_text":           [...] | None,
            "aug_tags":           [...] | None,
            "image_description":  [...] | None,
        }
    }
    """
    if not isinstance(data, dict):
        raise ValueError("embed() accepts a single dict only")

    preprocessed = build_inputs(
        text                = data.get("text", ""),
        tags                = data.get("tags", []),
        image_description   = data.get("image_description", ""),
    )

    vectors = embed_texts([
            preprocessed["text"],
            preprocessed["aug_text"],
            preprocessed["aug_tags"],
            preprocessed["image_description"],
        ])

    return {
        "preprocessed": {
            "text":               preprocessed["text"],
            "aug_text":           preprocessed["aug_text"],
            "aug_tags":           preprocessed["aug_tags"],
            "image_description":  preprocessed["image_description"],
        },
        "vectors": {
            "text":               vectors[0],
            "aug_text":           vectors[1],
            "aug_tags":           vectors[2],
            "image_description":  vectors[3],
        },
    }

__all__ = ["embed", "map_stats"]