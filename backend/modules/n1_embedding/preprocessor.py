"""
preprocessor.py
===============

Transforms raw user and location inputs into structured multi-channel
strings ready for embedding.

Signals are separated into independent channels to prevent cross-intent
contamination and to support multi-vector cosine retrieval.

────────────────────────────────────────────────────────────
USER OUTPUT STRUCTURE
────────────────────────────────────────────────────────────
{
    "expanded_emotion": str,   # emotion keyword expansions from text
    "expanded_context": str,   # context keyword expansions from text
    "expanded_tag":     str,   # tag expansions
    "expanded_image":   str,   # image description + visual keyword expansions
}

────────────────────────────────────────────────────────────
LOCATION OUTPUT STRUCTURE
────────────────────────────────────────────────────────────
{
    "expanded_text": str,   # description + emotion + context expansions
    "expanded_tag":  str,   # location tag expansions
}
"""

from __future__ import annotations

from .maps import scan_text, expand_tags, MatchResult


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def _expansions(matches: list[MatchResult]) -> list[str]:
    return [m.expansion for m in matches]


def build_user_input(text: str, image_description: str, tags: list[str]) -> dict[str, str]:

    # ── 1. Text → emotion + context channels ──────────────────
    text_scan = scan_text(text)

    emotion_kw = _dedupe(_expansions(text_scan["emotion"]))
    context_kw = _dedupe(_expansions(text_scan["context"]))

    expanded_emotion = " ".join(emotion_kw)
    expanded_context = " ".join(context_kw)

    # ── 2. Tags → independent signal ──────────────────────────
    tag_scan = expand_tags(tags)
    tag_kw = _dedupe(_expansions(tag_scan["tag"]))

    expanded_tag = " ".join(tag_kw)

    # ── 3. Image → independent visual channel ─────────────────
    if image_description:
        img_scan = scan_text(image_description)
        img_kw = _dedupe(
            _expansions(img_scan["emotion"]) +
            _expansions(img_scan["context"])
        )
        expanded_image = image_description.strip()
        if img_kw:
            expanded_image += " " + " ".join(img_kw)
    else:
        expanded_image = ""

    return {
        "expanded_emotion": expanded_emotion,
        "expanded_context": expanded_context,
        "expanded_tag":     expanded_tag,
        "expanded_image":   expanded_image,
    }


def build_location_input(description: str, tags: list[str]) -> dict[str, str]:

    # ── 1. Description → semantic expansion ───────────────────
    text_scan = scan_text(description)

    emotion_kw = _dedupe(_expansions(text_scan["emotion"]))
    context_kw = _dedupe(_expansions(text_scan["context"]))

    expanded_text = description.strip()
    if emotion_kw:
        expanded_text += " " + " ".join(emotion_kw)
    if context_kw:
        expanded_text += " " + " ".join(context_kw)

    # ── 2. Tags → explicit structured signal ──────────────────
    tag_scan = expand_tags(tags)
    tag_kw = _dedupe(_expansions(tag_scan["tag"]))

    expanded_tag = " ".join(tag_kw)

    return {
        "expanded_text": expanded_text,
        "expanded_tag":  expanded_tag,
    }