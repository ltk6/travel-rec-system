"""
embedder.py
===========

Loads and runs inference for the sentence embedding model used in
multi-vector semantic retrieval.

Converts multiple input strings (per semantic channel) into normalized
vector representations using a shared embedding model.

Recommended model: BAAI/bge-m3
  568M params · 1024-dim · 100+ languages · top VN-MTEB retrieval score

Drop-in alternatives (change MODEL_NAME only):
  AITeamVN/Vietnamese_Embedding   — BGE-M3 fine-tuned on 300k+ Vietnamese triplets
  intfloat/multilingual-e5-large  — 560M params, strong multilingual alternative
"""

from __future__ import annotations

from typing import List, Optional

MODEL_NAME = "BAAI/bge-m3"

try:
    from sentence_transformers import SentenceTransformer
    print(f"[Embedding] Loading '{MODEL_NAME}' into memory...")
    _MODEL = SentenceTransformer(MODEL_NAME)
    print(f"[Embedding] Ready. Device: {_MODEL.device}")
except ImportError:
    raise RuntimeError("sentence-transformers not installed")
except Exception as e:
    raise RuntimeError(f"Failed to load embedding model: {e}")


def get_model():
    """Return the globally loaded model."""
    return _MODEL


def embed_texts(texts: List[str]) -> List[Optional[List[float]]]:
    """
    Convert a list of strings into normalized embeddings.

    Empty or whitespace-only strings return None at their index.
    """
    model = get_model()

    if not texts:
        return []

    # Collect only non-empty texts, tracking their original indices
    valid_texts: List[str] = []
    valid_indices: List[int] = []

    for i, t in enumerate(texts):
        if t and t.strip():
            valid_texts.append(t)
            valid_indices.append(i)

    if not valid_texts:
        return [] * len(texts)

    vectors = model.encode(
        valid_texts,
        normalize_embeddings=True,
        batch_size=32,
        show_progress_bar=False,
    ).tolist()

    # Reconstruct full output list, inserting None for empty slots
    output: List[Optional[List[float]]] = [None] * len(texts)
    for vec, idx in zip(vectors, valid_indices):
        output[idx] = vec

    return output