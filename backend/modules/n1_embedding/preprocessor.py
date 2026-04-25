"""
preprocessor.py
===============

Transforms raw user and location inputs into structured multi-channel
strings ready for embedding.

Signals are separated into independent channels to prevent cross-intent
contamination and to support multi-vector cosine retrieval.

────────────────────────────────────────────────────────────
OUTPUT STRUCTURE
────────────────────────────────────────────────────────────
{
    "text":     str | None,   # text
    "aug_text": str | None,   # text + emotion + context keyword expansions
    "tag":      str | None,   # tag expansions
    "image":    str | None,   # image description
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


def build_inputs(
    text:               str | None,
    tags:               list[str] | None,
    image_description:  str | None
) -> dict[str, str | None]:

    # ── 0. Normalize inputs ──────────────────────────────────────
    text = (text or "").strip()
    tags = tags or []
    image_description = (image_description or "").strip()

    # ── 1. Text → emotion + context channels ──────────────────
    if text:
        text_scan = scan_text(text)

        emotion_kw = _dedupe(_expansions(text_scan["emotion"]))
        context_kw = _dedupe(_expansions(text_scan["context"]))

        expanded_emotion = " ".join(emotion_kw)
        expanded_context = " ".join(context_kw)

        parts = [text, expanded_emotion, expanded_context]
        expanded_text = " ".join(p for p in parts if p)
    else:
        expanded_text = ""

    # ── 2. Tags → independent signal ──────────────────────────
    if tags:
        tag_scan = expand_tags(tags)
        tag_kw = _dedupe(_expansions(tag_scan["tag"]))
        expanded_tag = " ".join(tag_kw)
    else:
        expanded_tag = ""

    return {
        "text":               text,
        "aug_text":           expanded_text,
        "aug_tags":           expanded_tag,
        "image_description":  image_description,
    }