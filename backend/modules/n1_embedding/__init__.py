"""
n1_module
=========
N1 – Text Embedding Module

Public API
----------
    from n1_embedding import embed, load_model

    model = load_model()   # call once at startup

    result = embed({
        "text": "Tôi muốn một chuyến đi yên tĩnh gần thiên nhiên",
        "image_description": "Peaceful misty highland, wooden structures",
        "tags": ["thiên nhiên", "yên tĩnh", "couple"]
    }, model=model)

    print(result["vector"])   # list[float], 1024-dim
"""

from __future__ import annotations

from .embedder     import load_model, _embed_text
from .preprocessor import build_enriched_text
from .maps         import stats as map_stats


def embed(data: dict, model=None) -> dict:
    """
    N1 main function — as specified by the system interface contract.

    Parameters
    ----------
    data : dict with keys:
        "text"              (str)       Free-text requirement, vi/en/mixed.
        "image_description" (str)       Plain English description from N2.
        "tags"              (list[str]) Quiz/user tags, vi/en/mixed.

    model : Pre-loaded SentenceTransformer (from load_model()).
            Pass None to use mock mode (for testing without GPU).

    Returns
    -------
    dict:
        "vector" : list[float]  Normalized 1024-dim embedding vector.
    """
    text              = data.get("text", "")
    image_description = data.get("image_description", "")
    tags              = data.get("tags", [])

    enriched = build_enriched_text(text, image_description, tags)
    vector   = _embed_text(enriched, model)

    return {"vector": vector}


__all__ = ["embed", "load_model", "map_stats"]