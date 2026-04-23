"""
─────────────────────────────────────────────
N2 — IMAGE UNDERSTANDING LAYER (VISION → SEMANTIC TEXT)
─────────────────────────────────────────────
INPUT:
{
    "image": bytes
}

OUTPUT:
{
    "image_description": str
}
"""

from .processor import process_image

__all__ = ['process_image']