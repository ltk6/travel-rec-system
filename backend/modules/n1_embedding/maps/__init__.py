"""
maps/
=====
Keyword mapping and enrichment module.
Sub-package containing dictionaries for tags, emotions, and context signals.
Exposes a unified registry for translating user inputs into embedding keywords.
"""

from .registry import scan_text, expand_tags, stats, MatchResult

__all__ = ["scan_text", "expand_tags", "stats", "MatchResult"]
