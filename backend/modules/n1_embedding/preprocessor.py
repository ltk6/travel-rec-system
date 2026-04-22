"""
preprocessor.py
===============

Transforms raw user and location inputs into structured multi-vector
embedding channels for retrieval and ranking.

The system separates semantic signals into independent channels to prevent
cross-intent contamination and to support multi-vector cosine retrieval.

Each channel is independently expanded using the shared semantic registry
(emotion, context, tags, image keywords).

────────────────────────────────────────────────────────────
USER OUTPUT STRUCTURE
────────────────────────────────────────────────────────────
{
    "expanded_emotion": str,   # text + emotion expansions
    "expanded_context": str,   # text + context expansions
    "expanded_tag": str,       # tag-derived keywords
    "expanded_image": str      # image + visual semantic expansions
}

────────────────────────────────────────────────────────────
LOCATION OUTPUT STRUCTURE
────────────────────────────────────────────────────────────
{
    "expanded_semantic": str,  # description + emotion + context expansions
    "expanded_tag": str        # location tags only
}
"""

from __future__ import annotations

from .maps import *


def _dedupe(items: list[str]) -> list[str]:
    """
    Remove duplicates while preserving order.
    Filters empty values and prioritizes first occurrence.
    """
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def _flatten(matches: list[MatchResult]) -> list[str]:
    """
    Extract expansion strings from MatchResult objects.
    """
    return [m.expansion for m in matches]


def build_user_input(
    text: str,
    image_description: str,
    tags: list[str],
) -> dict[str, str]:
    """
    Build user-side multi-channel embedding input.

    Channels:
    - emotion: intent + emotional expansion
    - context: situational expansion
    - tag: explicit preference signals
    - image: visual intent expansion
    """

    base_text = text.strip()

    # ─────────────────────────────
    # 1. TEXT → emotion + context
    # ─────────────────────────────
    text_scan = scan_text(text)

    emotion_kw = _dedupe(_flatten(text_scan["emotion"]))
    context_kw = _dedupe(_flatten(text_scan["context"]))

    expanded_emotion = " ".join([base_text] + emotion_kw) if base_text else " ".join(emotion_kw)
    expanded_context = " ".join([base_text] + context_kw) if base_text else " ".join(context_kw)

    # ─────────────────────────────
    # 2. TAGS → independent signal
    # ─────────────────────────────
    tag_scan = expand_tags(tags)
    tag_kw = _dedupe(_flatten(tag_scan["tag"]))

    expanded_tag = " ".join(tag_kw)

    # ─────────────────────────────
    # 3. IMAGE → independent visual channel
    # ─────────────────────────────
    if image_description:
        img_scan = scan_text(image_description)

        img_kw = _dedupe(
            _flatten(img_scan["emotion"]) +
            _flatten(img_scan["context"])
        )

        expanded_image = image_description.strip()

        if img_kw:
            expanded_image += " " + " ".join(img_kw)
    else:
        expanded_image = ""

    return {
        "expanded_emotion": expanded_emotion,
        "expanded_context": expanded_context,
        "expanded_tag": expanded_tag,
        "expanded_image": expanded_image,
    }


def build_location_input(description: str, tags: list[str]) -> dict[str, str]:
    """
    Build location-side embedding representation.

    The location is treated as a document entity:
    - semantic channel = description + emotion/context expansions
    - tag channel = explicit structured tags
    """

    # ─────────────────────────────
    # 1. DESCRIPTION → semantic expansion
    # ─────────────────────────────
    text_scan = scan_text(description)

    emotion_kw = _dedupe(_flatten(text_scan["emotion"]))
    context_kw = _dedupe(_flatten(text_scan["context"]))

    expanded_semantic = description.strip()

    if emotion_kw:
        expanded_semantic += " " + " ".join(emotion_kw)

    if context_kw:
        expanded_semantic += " " + " ".join(context_kw)

    # ─────────────────────────────
    # 2. TAGS → explicit structured signal
    # ─────────────────────────────
    tag_scan = expand_tags(tags)
    expanded_tag = " ".join(_flatten(tag_scan["tag"]))

    return {
        "expanded_semantic": expanded_semantic,
        "expanded_tag": expanded_tag,
    }