"""
embedder.py
===========

Handles loading and inference for the sentence embedding model used in
multi-vector semantic retrieval.

This module converts multiple input strings (per semantic channel)
into normalized vector representations using a shared embedding model.

Recommended: BAAI/bge-m3
  568M params, 1024-dim, 100+ languages, top VN-MTEB retrieval score.

Drop-in alternatives (change MODEL_NAME only):
  AITeamVN/Vietnamese_Embedding   BGE-M3 fine-tuned on 300k+ Vietnamese triplets
  intfloat/multilingual-e5-large  560M, strong multilingual alternative
"""

from __future__ import annotations

from typing import List

MODEL_NAME = "BAAI/bge-m3"

_MODEL = None


def get_model():
    """
    Returns the globally cached model.
    Loads it on first call (lazy loading).
    """
    global _MODEL

    if _MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer

            print(f"[Embedder] Loading '{MODEL_NAME}' into memory...")
            _MODEL = SentenceTransformer(MODEL_NAME)

            print(f"[Embedder] Ready. Device: {_MODEL.device}")

        except ImportError:
            print("[Embedder] Error: sentence-transformers not installed.")
        except Exception as e:
            print(f"[Embedder] Load failed: {e}")

    return _MODEL


# preload model once
print(f"[Embedder] Initializing '{MODEL_NAME}'")
get_model()


from typing import List, Optional

def embed_texts(texts: List[str]) -> List[Optional[List[float]]]:
    """
    Convert list of strings into embeddings.

    Empty or whitespace-only strings → None
    """

    model = get_model()

    if model is None or not texts:
        return []

    # ─────────────────────────────
    # 1. Normalize + mark empty
    # ─────────────────────────────
    cleaned_texts: List[str] = []
    index_map: List[int] = []

    for i, t in enumerate(texts):
        if t is None or not t.strip():
            continue
        cleaned_texts.append(t)
        index_map.append(i)

    # if everything is empty
    if not cleaned_texts:
        return [None] * len(texts)

    # ─────────────────────────────
    # 2. Embed only valid texts
    # ─────────────────────────────
    vectors = model.encode(
        cleaned_texts,
        normalize_embeddings=True,
        batch_size=32,
        show_progress_bar=False,
    ).tolist()

    # ─────────────────────────────
    # 3. Reconstruct full output with None gaps
    # ─────────────────────────────
    output: List[Optional[List[float]]] = [None] * len(texts)

    for vec, idx in zip(vectors, index_map):
        output[idx] = vec

    return output