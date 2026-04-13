"""
n1_module
=========
N1 – Text Embedding Module

Public API
----------
    from n1_embedding import embed

    result = embed({
        "text": "Tôi muốn một chuyến đi yên tĩnh gần thiên nhiên",
        "image_description": "Peaceful misty highland, wooden structures",
        "tags": ["thiên nhiên", "yên tĩnh", "couple"]
    })

    print(result["vector"])   # list[float], 1024-dim
"""

from __future__ import annotations

from .embedder     import embed_text, get_model
from .preprocessor import build_enriched_text
from .maps         import stats as map_stats


def embed(data: dict) -> dict:
    """
    N1 main function — as specified by the system interface contract.

    Parameters
    ----------
    data : dict with keys:
        "text"              (str)       Free-text requirement, vi/en/mixed.
        "image_description" (str)       Plain English description from N2.
        "tags"              (list[str]) Quiz/user tags, vi/en/mixed.

    Returns
    -------
    dict:
        "vector" : list[float]  Normalized 1024-dim embedding vector.
    """
    text              = data.get("text", "")
    image_description = data.get("image_description", "")
    tags              = data.get("tags", [])

    enriched = build_enriched_text(text, image_description, tags)
    vector   = embed_text(enriched)

    return {"vector": vector}


__all__ = ["embed", "get_model", "map_stats"]
