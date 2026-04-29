"""
Transforms raw inputs into multi-channel strings for embedding.
Each channel is kept independent to prevent cross-intent contamination.
Returns preprocessed texts and kw_exp_count (total keyword expansions found).
"""

from __future__ import annotations

from .maps import scan_text, expand_tags, MatchResult


def _dedupe(items: list[str]) -> list[str]:
    """Remove duplicates while preserving order, skip blanks."""
    seen: set[str] = set()
    return [seen.add(x) or x for x in items if x and x not in seen]


def _expansions(matches: list[MatchResult]) -> list[str]:
    """Extract expansion strings from match results."""
    return [m.expansion for m in matches]


def build_inputs(
    text:     str,
    tags:     list[str],
    img_desc: str,
) -> dict:
    """
    Build all preprocessed channels and count keyword expansions.

    Returns dict with keys: text, aug_text, aug_tags, img_desc, kw_count.
    kw_count = total number of unique keywords detected in text.
    """
    text = (text or "").strip()
    tags = tags or []
    img_desc = (img_desc or "").strip()
    kw_count = 0

    # Text → emotion + context keyword expansion
    if text:
        scan = scan_text(text)
        emotion_kw = _dedupe(_expansions(scan["emotion"]))
        context_kw = _dedupe(_expansions(scan["context"]))
        kw_count += len(emotion_kw) + len(context_kw)
        parts = [text, " ".join(emotion_kw), " ".join(context_kw)]
        aug_text = " ".join(p for p in parts if p)
    else:
        aug_text = ""

    # Tags → independent tag expansion
    if tags:
        tag_scan = expand_tags(tags)
        tag_kw = _dedupe(_expansions(tag_scan["tag"]))
        aug_tags = " ".join(tag_kw)
    else:
        aug_tags = ""

    return {
        "text":     text,
        "aug_text": aug_text,
        "aug_tags": aug_tags,
        "img_desc": img_desc,
        "kw_count": kw_count,
    }