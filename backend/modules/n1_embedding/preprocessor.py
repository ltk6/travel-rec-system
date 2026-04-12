"""
preprocessor.py
===============
Enriches raw N8 input into a single embedding-ready string.

Pipeline
--------
1. Scan user text for emotion + context signals
2. Expand tags (vi → en travel keywords)
3. Assemble image description into a sentence
4. Join everything into one ordered prompt string
"""

from __future__ import annotations

from .maps.registry import scan_text, expand_tags, MatchResult


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out:  list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def _image_desc_to_text(image_description: str) -> str:
    return image_description.strip() if image_description else ""


def build_enriched_text(
    text:              str,
    image_description: str,
    tags:              list[str],
) -> str:
    """
    Enrich and assemble inputs into a single prompt string for BGE-M3.

    Parameters
    ----------
    text              : Free-text requirement from user (vi / en / mixed).
    image_description : Plain English description string from N2.
    tags              : Tag list from quiz (vi / en / mixed).

    Returns
    -------
    Single enriched string ready for embedding.
    """
    # ── 1. Scan free text for emotion + context signals
    text_matches: list[MatchResult] = scan_text(text)
    if image_description:
        text_matches += scan_text(image_description)

    expansions = _dedupe([m.expansion for m in text_matches])

    # ── 2. Expand tags
    tag_matches   = expand_tags(tags)
    tag_keywords  = _dedupe([m.expansion for m in tag_matches])

    # ── 3. Assemble parts in priority order:
    #    user intent → image context → tags → signal expansions
    parts: list[str] = []

    if text.strip():
        parts.append(f"User requirement: {text.strip()}")

    img = _image_desc_to_text(image_description)
    if img:
        parts.append(f"Desired scene: {img}")

    if tag_keywords:
        parts.append(f"Keywords: {', '.join(tag_keywords)}")

    if expansions:
        parts.append(f"Context: {' | '.join(expansions)}")

    return ". ".join(parts)