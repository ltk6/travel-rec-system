"""
maps/registry.py
================

Core keyword registry and semantic extraction engine for N1 preprocessing.

Provides high-performance lookup and matching for:
  - Emotion signals  (user mood → travel intent keywords)
  - Context signals  (situational constraints → grounding keywords)
  - Tag signals      (explicit user preferences → travel descriptors)

Responsible only for extraction and expansion — does not build embeddings
or final vectors.

────────────────────────────────────────────────────────────
SECTION INDEX
────────────────────────────────────────────────────────────
  A. MAP REGISTRATION   — load and normalize emotion/context/tag maps
  B. MATCH RESULT TYPE  — structured match output (source, key, expansion)
  C. TEXT SCANNING      — emotion + context extraction with deduplication
  D. TAG EXPANSION      — tag normalization and enrichment
  E. UTILITIES          — stats
"""

from __future__ import annotations

from typing import NamedTuple

from .emotions import ALL_EMOTIONS
from .tags import ALL_TAGS
from .context import ALL_CONTEXT


# ── Lowercased lookup tables built once at import ─────────────────────────────
_EMOTIONS: dict[str, str] = {k.lower().strip(): v for k, v in ALL_EMOTIONS.items()}
_TAGS:     dict[str, str] = {k.lower().strip(): v for k, v in ALL_TAGS.items()}
_CONTEXT:  dict[str, str] = {k.lower().strip(): v for k, v in ALL_CONTEXT.items()}


class MatchResult(NamedTuple):
    source:    str   # "emotion" | "context" | "tag" | "tag_passthrough"
    key:       str   # phrase that matched
    expansion: str   # travel keywords produced


def _dedupe_substrings(matches: list[MatchResult]) -> list[MatchResult]:
    """Keep only the longest match when one key is a substring of another."""
    kept: list[MatchResult] = []
    for m in sorted(matches, key=lambda m: len(m.key), reverse=True):
        if not any(m.key in k.key for k in kept):
            kept.append(m)
    return kept


# ── Public API ────────────────────────────────────────────────────────────────

def scan_text(text: str) -> dict[str, list[MatchResult]]:
    """
    Scan free text and return matched signals grouped by channel.

    Returns:
        {
            "emotion": [...],
            "context": [...],
        }

    Uses substring matching with longest-match deduplication.
    """
    normed = text.lower().strip()

    emotion_hits = [
        MatchResult("emotion", key, _EMOTIONS[key])
        for key in _EMOTIONS if key in normed
    ]
    context_hits = [
        MatchResult("context", key, _CONTEXT[key])
        for key in _CONTEXT if key in normed
    ]

    return {
        "emotion": _dedupe_substrings(emotion_hits),
        "context": _dedupe_substrings(context_hits),
    }


def expand_tags(tags: list[str]) -> dict[str, list[MatchResult]]:
    """
    Expand a list of tags into keyword strings.

    Known tags are expanded via the tag map.
    Unknown tags are passed through as-is.

    Returns:
        {
            "tag":              [...],   # matched and expanded
            "tag_passthrough":  [...],   # unrecognised, passed through raw
        }
    """
    expanded:    list[MatchResult] = []
    passthrough: list[MatchResult] = []

    for tag in tags:
        key = tag.lower().strip()
        if key in _TAGS:
            expanded.append(MatchResult("tag", tag, _TAGS[key]))
        else:
            passthrough.append(MatchResult("tag_passthrough", tag, tag))

    return {
        "tag":             expanded,
        "tag_passthrough": passthrough,
    }


def stats() -> str:
    """Return a formatted summary of registry coverage."""
    lines = [
        "── Map Registry ─────────────────────────────────────────",
        f"  Emotions : {len(_EMOTIONS):>3}",
        f"  Tags     : {len(_TAGS):>3}",
        f"  Context  : {len(_CONTEXT):>3}",
        "  ─────────────────────────────────────────────────────",
        f"  Total    : {len(_EMOTIONS) + len(_TAGS) + len(_CONTEXT):>3}",
        "─────────────────────────────────────────────────────────",
    ]
    return "\n".join(lines)