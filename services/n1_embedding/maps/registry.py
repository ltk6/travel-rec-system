"""
maps/registry.py
================
Unified registry for all keyword maps.
Exposes a single lookup API used by the preprocessor.

Three active maps:
  - tags     : vi/en tag → enriched English travel keywords
  - emotions : emotional state → travel style keywords
  - context  : season/weather + social group → travel keywords
"""

from __future__ import annotations
from typing import NamedTuple

from .emotions import ALL_EMOTIONS
from .tags     import ALL_TAGS
from .context  import ALL_CONTEXT


# ── Build lowercased lookup tables once at import
_EMOTIONS: dict[str, str] = {k.lower().strip(): v for k, v in ALL_EMOTIONS.items()}
_TAGS:     dict[str, str] = {k.lower().strip(): v for k, v in ALL_TAGS.items()}
_CONTEXT:  dict[str, str] = {k.lower().strip(): v for k, v in ALL_CONTEXT.items()}

# Full-text scan map (emotions + context only — tags operate on a list)
_FULLTEXT: dict[str, str] = {**_EMOTIONS, **_CONTEXT}


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
    lines = [
        "── Map Registry ────────────────────────",
        f"  Emotions  : {len(_EMOTIONS):>3} entries",
        f"  Tags      : {len(_TAGS):>3} entries",
        f"  Context   : {len(_CONTEXT):>3} entries",
        f"  Total     : {len(_EMOTIONS) + len(_TAGS) + len(_CONTEXT):>3} entries",
        "────────────────────────────────────────",
    ]
    return "\n".join(lines)