"""
maps/registry.py
================
Unified registry and lookup API for all keyword mapping sub-modules.
Serves as the primary interface for the N1 preprocessor.

This module centralizes 'tags', 'emotions', and 'context' maps into a single 
high-performance lookup system with unified results.

─────────────────────────────────────────────────────────────
SECTION INDEX
─────────────────────────────────────────────────────────────
  A. MAP REGISTRATION  — importing and merging sub-modules
  B. LOOKUP TABLES     — pre-compiled lowercased dictionaries
  C. MATCH RESULT TYPE — structured data for mapping results
  D. PUBLIC API        — scan_text, expand_tags, stats()

REGISTRY COVERAGE
──────────────────────────────────────────────────────────────────────────
  • TAGS     : Normalizes vi/en quiz tags into travel keywords.
  • EMOTIONS : Maps user sentiment/mood to trip archetypes.
  • CONTEXT  : Translates situational signals into trip grounding.
──────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations
from typing import NamedTuple

from .emotions import (
    ALL_EMOTIONS,
    EXHAUSTION_STRESS,
    BOREDOM,
    SADNESS,
    ROMANCE,
    CURIOSITY,
    EXCITEMENT,
    NOSTALGIA,
    SOCIAL_FATIGUE,
)
from .tags import (
    ALL_TAGS,
    NATURE_TAGS,
    URBAN_TAGS,
    ACTIVITY_TAGS,
    ACCOMMODATION_TAGS,
    ATMOSPHERE_TAGS,
    TRIP_STYLE_TAGS,
    CONSTRAINT_TAGS,
)
from .context import (
    ALL_CONTEXT,
    SEASON_WEATHER,
    SOCIAL_GROUP,
    TRIP_DURATION,
    TRIP_DISTANCE,
    BUDGET_LEVEL,
    PACE,
)


# ── Build lowercased lookup tables once at import
_EMOTIONS: dict[str, str] = {k.lower().strip(): v for k, v in ALL_EMOTIONS.items()}
_TAGS:     dict[str, str] = {k.lower().strip(): v for k, v in ALL_TAGS.items()}
_CONTEXT:  dict[str, str] = {k.lower().strip(): v for k, v in ALL_CONTEXT.items()}

# Full-text scan map (emotions + context — tags operate on explicit list)
_FULLTEXT: dict[str, str] = {**_EMOTIONS, **_CONTEXT}

# Per-section counts for stats()
_TAG_SECTIONS: dict[str, int] = {
    "Nature / Landscape":   len(NATURE_TAGS),
    "Urban / Culture":      len(URBAN_TAGS),
    "Activities":           len(ACTIVITY_TAGS),
    "Accommodation":        len(ACCOMMODATION_TAGS),
    "Atmosphere / Vibe":    len(ATMOSPHERE_TAGS),
    "Trip Style":           len(TRIP_STYLE_TAGS),
    "Constraints":          len(CONSTRAINT_TAGS),
}
_EMOTION_SECTIONS: dict[str, int] = {
    "Exhaustion / Stress":  len(EXHAUSTION_STRESS),
    "Boredom":              len(BOREDOM),
    "Sadness":              len(SADNESS),
    "Romance":              len(ROMANCE),
    "Curiosity":            len(CURIOSITY),
    "Excitement":           len(EXCITEMENT),
    "Nostalgia":            len(NOSTALGIA),
    "Social Fatigue":       len(SOCIAL_FATIGUE),
}
_CONTEXT_SECTIONS: dict[str, int] = {
    "Season / Weather":     len(SEASON_WEATHER),
    "Social Group":         len(SOCIAL_GROUP),
    "Trip Duration":        len(TRIP_DURATION),
    "Trip Distance":        len(TRIP_DISTANCE),
    "Budget Level":         len(BUDGET_LEVEL),
    "Pace":                 len(PACE),
}


class MatchResult(NamedTuple):
    source:    str   # "emotion" | "context" | "tag" | "tag_passthrough"
    key:       str   # phrase that matched
    expansion: str   # travel keywords produced


# ─────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────

def scan_text(text: str) -> list[MatchResult]:
    """
    Scan free text (user_text or image_description) against
    emotion and context maps. Returns all matches found.
    """
    normed  = text.lower().strip()
    results: list[MatchResult] = []

    for key, expansion in _EMOTIONS.items():
        if key in normed:
            results.append(MatchResult("emotion", key, expansion))

    for key, expansion in _CONTEXT.items():
        if key in normed:
            results.append(MatchResult("context", key, expansion))

    return results


def expand_tags(tags: list[str]) -> list[MatchResult]:
    """
    Translate/expand a list of tags.
    Known tags → enriched English keywords.
    Unknown tags → passed through unchanged.
    """
    results: list[MatchResult] = []
    for tag in tags:
        key = tag.lower().strip()
        if key in _TAGS:
            results.append(MatchResult("tag", tag, _TAGS[key]))
        else:
            results.append(MatchResult("tag_passthrough", tag, tag))
    return results


def stats() -> str:
    def section_block(sections: dict[str, int]) -> str:
        return "\n".join(
            f"    {name:<22}: {count:>3}" for name, count in sections.items()
        )

    total = len(_EMOTIONS) + len(_TAGS) + len(_CONTEXT)
    lines = [
        "── Map Registry ─────────────────────────────────────────",
        f"  Emotions  : {len(_EMOTIONS):>3} entries (8 sections)",
        section_block(_EMOTION_SECTIONS),
        f"  Tags      : {len(_TAGS):>3} entries (7 sections)",
        section_block(_TAG_SECTIONS),
        f"  Context   : {len(_CONTEXT):>3} entries (6 sections)",
        section_block(_CONTEXT_SECTIONS),
        f"  ─────────────────────────────────────────────────────",
        f"  Total     : {total:>3} entries",
        "─────────────────────────────────────────────────────────",
    ]
    return "\n".join(lines)