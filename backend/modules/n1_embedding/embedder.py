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


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Convert a list of strings into a list of normalized vectors.

    Input:
        ["text A", "text B", ...]

    Output:
        [[1024-dim vector], [1024-dim vector], ...]
    """
    model = get_model()

    if model is None or not texts:
        return []

    vectors = model.encode(
        texts,
        normalize_embeddings=True,
        batch_size=32,
        show_progress_bar=False,
    )

    return vectors.tolist()