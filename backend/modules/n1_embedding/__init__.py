"""
n1_embedding — Unified embedding API.
Preprocesses multi-channel inputs, generates vectors, and returns signal metadata.
"""

from __future__ import annotations

from typing import Dict, Any

from .embedder import embed_texts
from .preprocessor import build_inputs

def embed(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Single entry point for the embedding pipeline.

    Input:  { text, tags, img_desc }
    Output: { preprocessed, vectors, sig_k }

    sig_k = keyword expansion signal strength (count of expansions detected).
    """
    if not isinstance(data, dict):
        raise ValueError("embed() accepts a single dict only")

    preprocessed = build_inputs(
        text     = data.get("text", ""),
        tags     = data.get("tags", []),
        img_desc = data.get("img_desc", ""),
    )

    # Channel order: text, aug_text, aug_tags, img_desc
    channels = ["text", "aug_text", "aug_tags", "img_desc"]
    vectors = embed_texts([preprocessed[ch] for ch in channels])

    return {
        "sig_k":        preprocessed["kw_count"],
        "preprocessed": {
            "text":     preprocessed["text"],
            "aug_text": preprocessed["aug_text"],
            "aug_tags": preprocessed["aug_tags"],
            "img_desc": preprocessed["img_desc"],
        },
        "vectors": {
            "text":     vectors[0],
            "aug_text": vectors[1],
            "aug_tags": vectors[2],
            "img_desc": vectors[3],
        },  
    }

__all__ = ["embed"]