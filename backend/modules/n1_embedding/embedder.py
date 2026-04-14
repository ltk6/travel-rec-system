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

MODEL_NAME = "BAAI/bge-m3"

_MODEL = None

def get_model():
    """
    Returns the globally cached model. 
    Loads it on the first call (Lazy Loading).
    """
    global _MODEL
    if _MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer
            print(f"[Embedder] Loading '{MODEL_NAME}' into memory...")
            _MODEL = SentenceTransformer(MODEL_NAME)
            print(f"[Embedder] Ready. Device: {_MODEL.device}")
        except ImportError:
            print("[Embedder] Error: 'sentence-transformers' not installed.")
        except Exception as e:
            print(f"[Embedder] Load failed: {e}")
    return _MODEL

# Load model once upon import
print(f"[Embedder] Getting '{MODEL_NAME}'")
get_model()

def embed_text(text: str) -> list[float]:
    """
    Convert a string to a normalized vector using the global model.
    Returns an empty list if the model fails to load.
    """
    model = get_model()
    if model is not None:
        # BGE-M3 works best with normalized embeddings for cosine similarity
        vec = model.encode(text, normalize_embeddings=True)
        return vec.tolist()
    return []
