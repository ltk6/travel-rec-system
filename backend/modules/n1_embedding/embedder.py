"""
embedder.py
===========
Model loading and text → vector conversion.

Recommended: BAAI/bge-m3
  568M params, 1024-dim, 100+ languages, top VN-MTEB retrieval score.

Drop-in alternatives (change MODEL_NAME only):
  AITeamVN/Vietnamese_Embedding   BGE-M3 fine-tuned on 300k+ Vietnamese triplets
  intfloat/multilingual-e5-large  560M, strong multilingual alternative
"""

from __future__ import annotations
import hashlib
import math

MODEL_NAME = "BAAI/bge-m3"


def load_model(model_name: str = MODEL_NAME):
    """Load SentenceTransformer model."""
    try:
        from sentence_transformers import SentenceTransformer
        print(f"[Embedder] Loading '{model_name}' ...")
        model = SentenceTransformer(model_name)
        print(f"[Embedder] Ready. Max seq length: {model.max_seq_length}")
        return model
    except ImportError:
        print("[Embedder] sentence-transformers not installed.")
        return None
    except Exception as e:
        print(f"[Embedder] Load failed ({e}).")
        return None


def _embed_text(text: str, model) -> list[float]:
    """Convert a string to a normalized vector."""
    if model is not None:
        vec = model.encode(text, normalize_embeddings=True)
        return vec.tolist()