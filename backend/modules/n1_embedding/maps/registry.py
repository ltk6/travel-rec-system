"""
maps/registry.py
================

Core keyword registry and semantic extraction engine for N8 preprocessing.

This module provides high-performance lookup and matching for:
- Emotion signals (user mood → travel intent keywords)
- Context signals (situational constraints → grounding keywords)
- Tag signals (explicit user preferences → travel descriptors)

It is responsible ONLY for extraction and expansion.
It does NOT build embeddings or final vectors.

─────────────────────────────────────────────────────────────
SECTION INDEX
─────────────────────────────────────────────────────────────
  A. MAP REGISTRATION   — load and normalize emotion/context/tag maps
  B. LOOKUP TABLES      — lowercased high-speed dictionaries
  C. MATCH RESULT TYPE  — structured match output (source, key, expansion)
  D. TEXT SCANNING      — emotion + context extraction with deduplication
  E. TAG EXPANSION      — tag normalization and enrichment
  F. UTILITIES          — stats + internal helpers

REGISTRY COVERAGE
─────────────────────────────────────────────────────────────
  • EMOTIONS : maps free-text mood → semantic travel intent keywords
  • CONTEXT  : maps situational cues → travel constraint/setting keywords
  • TAGS     : maps explicit user preferences → curated travel descriptors
"""

from __future__ import annotations
from typing import NamedTuple

from .emotions import ALL_EMOTIONS
from .tags import ALL_TAGS
from .context import ALL_CONTEXT

# ── Build lowercased lookup tables once at import
_EMOTIONS: dict[str, str] = {k.lower().strip(): v for k, v in ALL_EMOTIONS.items()}
_TAGS:     dict[str, str] = {k.lower().strip(): v for k, v in ALL_TAGS.items()}
_CONTEXT:  dict[str, str] = {k.lower().strip(): v for k, v in ALL_CONTEXT.items()}

class MatchResult(NamedTuple):
    source:    str   # "emotion" | "context" | "tag" | "tag_passthrough"
    key:       str   # phrase that matched
    expansion: str   # travel keywords produced

# ── Internal: dedupe substrings (prefer longer phrases) ─────
def _dedupe_substrings(matches: list[MatchResult]) -> list[MatchResult]:
    matches_sorted = sorted(matches, key=lambda m: len(m.key), reverse=True)

    kept: list[MatchResult] = []

    for m in matches_sorted:
        if not any(m.key in k.key for k in kept):
            kept.append(m)

    return kept

# ─────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────

def scan_text(text: str) -> dict[str, list[MatchResult]]:
    """
    Scan free text into structured channels:
        {
            "emotion": [...],
            "context": [...]
        }

    • Simple substring scan
    • Post-deduplication (longest match wins)
    """
    normed = text.lower().strip()

    emotion_results = [
        MatchResult("emotion", key, _EMOTIONS[key])
        for key in _EMOTIONS
        if key in normed
    ]

    context_results = [
        MatchResult("context", key, _CONTEXT[key])
        for key in _CONTEXT
        if key in normed
    ]

    return {
        "emotion": _dedupe_substrings(emotion_results),
        "context": _dedupe_substrings(context_results),
    }


def expand_tags(tags: list[str]) -> dict[str, list[MatchResult]]:
    """
    Expand tags into:
        {
            "tag": [...],
            "tag_passthrough": [...]
        }
    """
    expanded: list[MatchResult] = []
    passthrough: list[MatchResult] = []

    for tag in tags:
        key = tag.lower().strip()

        if key in _TAGS:
            expanded.append(MatchResult("tag", tag, _TAGS[key]))
        else:
            passthrough.append(MatchResult("tag_passthrough", tag, tag))

    return {
        "tag": expanded,
        "tag_passthrough": passthrough,
    }

def stats() -> str:
    """
    Simple registry stats overview.
    """

    emotions = len(_EMOTIONS)
    tags     = len(_TAGS)
    context  = len(_CONTEXT)
    total    = emotions + tags + context

    lines = [
        "── Map Registry ─────────────────────────────────────────",
        f"  Emotions : {emotions:>3}",
        f"  Tags     : {tags:>3}",
        f"  Context  : {context:>3}",
        "  ─────────────────────────────────────────────────────",
        f"  Total    : {total:>3}",
        "─────────────────────────────────────────────────────────",
    ]

    return "\n".join(lines)