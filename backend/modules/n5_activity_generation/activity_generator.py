# =============================================================================
# activity_generator.py
# =============================================================================
# N5 — Activity Generation Module (Sequential LLM Pipeline).
#
# Flow per location:
#   1. Pull ground-truth templates from ACTIVITY_TEMPLATES.
#   2. Compute how many activities to ask the LLM for (respects LLM_RATIO).
#   3. If LLM_RATIO < 1.0, promote template activities verbatim to fill the gap.
#   4. Call LLM → validate → deduplicate → build canonical output objects.
# =============================================================================

import hashlib
import logging
import time
from typing import Any, Dict, List, Optional, Tuple

from .activity_templates import ACTIVITY_TEMPLATES
from .config import (
    DEFAULT_TARGET_PER_LOCATION,
    INTER_REQUEST_DELAY_S,
    LLM_RATIO,
    MAX_TARGET_PER_LOCATION,
    VALID_ACTIVITY_TYPES,
)

try:
    from .llm_generator import generate_activities_for_location, is_llm_available
    _LLM_IMPORT_OK = True
except ImportError:
    _LLM_IMPORT_OK = False
    def is_llm_available() -> bool: return False
    def generate_activities_for_location(*a, **kw) -> List: return []

logger = logging.getLogger("N5.Generator")


# =============================================================================
# PUBLIC ENTRY POINT
# =============================================================================

def generate_activities(data: dict) -> dict:
    """
    Core entry point consumed by the pipeline.

    Expected input schema: see __init__.py
    Returns: {"activities": [<canonical activity objects>]}
    """
    user, locations, constraints, target_count = _parse_input(data)
    target_count = min(target_count, MAX_TARGET_PER_LOCATION)

    all_activities: List[Dict] = []

    if not _LLM_IMPORT_OK or not is_llm_available():
        logger.error(
            "N5 halted: LLM unavailable (missing API key or import failure). "
            "Set GROQ_API_KEY in environment."
        )
        return {"activities": []}

    logger.info(
        "N5 START — %d location(s), target %d activities/loc, LLM_RATIO=%.2f",
        len(locations), target_count, LLM_RATIO,
    )

    for idx, loc in enumerate(locations):
        loc_id   = loc["location_id"]
        loc_name = loc["metadata"].get("name", "Unknown")
        loc_desc = loc["metadata"].get("description", "")

        logger.info("[%d/%d] %s (%s)", idx + 1, len(locations), loc_name, loc_id)

        templates = ACTIVITY_TEMPLATES.get(loc_id, [])
        if templates:
            logger.debug("  Templates found: %d", len(templates))
        else:
            logger.warning("  No templates for %s — LLM generating from scratch.", loc_id)

        # ── Determine how many the LLM should generate ───────────────────────
        llm_target   = max(1, round(target_count * LLM_RATIO))
        tmpl_slots   = target_count - llm_target        # activities to take verbatim from templates

        t0 = time.time()
        llm_acts: List[Dict] = []

        try:
            llm_acts = generate_activities_for_location(
                location     = {"name": loc_name, "description": loc_desc},
                user_text    = user.get("text", ""),
                user_tags    = user.get("tags", []),
                target_count = llm_target,
                templates    = templates,
            )
        except Exception as exc:
            logger.error("  LLM call failed for %s: %s", loc_id, exc)

        elapsed = time.time() - t0
        logger.info("  LLM returned %d activities in %.2fs", len(llm_acts), elapsed)

        # ── Optionally backfill with template stubs (when LLM_RATIO < 1.0) ──
        tmpl_acts: List[Dict] = []
        if tmpl_slots > 0 and templates:
            for t in templates[:tmpl_slots]:
                tmpl_acts.append(_stub_from_template(t))
            logger.debug("  Backfilled %d template stubs", len(tmpl_acts))

        # ── Merge, deduplicate, cap ──────────────────────────────────────────
        combined  = _deduplicate(llm_acts + tmpl_acts)
        combined  = combined[:target_count]

        if len(combined) < target_count:
            logger.warning(
                "  Only %d/%d activities for %s after dedup",
                len(combined), target_count, loc_id,
            )

        # ── Build canonical output objects ───────────────────────────────────
        for j, act_data in enumerate(combined):
            activity = _build_output(
                activity_id = _make_id(loc_id, j),
                location_id = loc_id,
                act_data    = act_data,
            )
            all_activities.append(activity)

        # ── Pacing ───────────────────────────────────────────────────────────
        if idx < len(locations) - 1:
            logger.debug("  Pacing: %.1fs before next location", INTER_REQUEST_DELAY_S)
            time.sleep(INTER_REQUEST_DELAY_S)

    logger.info("N5 DONE — %d total activities across %d locations", len(all_activities), len(locations))
    return {"activities": all_activities}


# =============================================================================
# INPUT PARSING
# =============================================================================

def _parse_input(data: dict) -> Tuple[Dict, List[Dict], Dict, int]:
    user        = data.get("user", {}) or {}
    locations   = data.get("locations", []) or []
    constraints = data.get("constraints", {}) or {}
    target      = int(data.get("target_count", DEFAULT_TARGET_PER_LOCATION))

    # Normalise user tags to lowercase strings
    raw_tags = user.get("tags") or []
    if isinstance(raw_tags, str):
        raw_tags = [t.strip() for t in raw_tags.split(",") if t.strip()]
    user["tags"] = [str(t).lower().strip() for t in raw_tags]

    return user, locations, constraints, target


# =============================================================================
# OUTPUT BUILDER
# =============================================================================

def _build_output(activity_id: str, location_id: str, act_data: Dict) -> Dict:
    """
    Maps a validated act_data dict into the canonical N5 output schema.
    All fields defined in __init__.py are populated; none are dropped.
    """
    return {
        "activity_id": activity_id,
        "location_id": location_id,
        "metadata": {
            # ── Core Identity ────────────────────────────────────────────────
            "name":                 act_data.get("name", "N/A"),
            "description":          act_data.get("description", ""),

            # ── Semantic Classification ──────────────────────────────────────
            "tags":                 act_data.get("tags", []),
            "activity_type":        act_data.get("activity_type", "nature"),
            "activity_subtype":     act_data.get("activity_subtype"),          # may be None

            # ── Experience Dynamics ──────────────────────────────────────────
            "intensity":            act_data.get("intensity", 0.5),
            "physical_level":       act_data.get("physical_level", 0.3),
            "social_level":         act_data.get("social_level", 0.5),

            # ── Constraint Fit ───────────────────────────────────────────────
            "estimated_duration":   act_data.get("estimated_duration", 90),
            "price_level":          act_data.get("price_level", 2.0),
            "indoor_outdoor":       act_data.get("indoor_outdoor", "outdoor"),
            "weather_dependent":    act_data.get("weather_dependent", True),

            # ── Context Fit Signals ──────────────────────────────────────────
            "time_of_day_suitable": act_data.get("time_of_day_suitable", "anytime"),
        },
    }


# =============================================================================
# TEMPLATE STUB CONVERTER
# =============================================================================

def _stub_from_template(template: Dict) -> Dict:
    """
    Converts a minimal template entry into a partial act_data dict.
    Used when LLM_RATIO < 1.0 and we need to backfill with template activities.
    The stub carries just enough for _build_output to produce a usable record.
    """
    t_type = template.get("type", "nature")
    if t_type not in VALID_ACTIVITY_TYPES:
        t_type = "nature"

    return {
        "name":                 template.get("name", "N/A"),
        "description":          "",      # no description available from raw template
        "tags":                 [],
        "activity_type":        t_type,
        "activity_subtype":     None,
        "intensity":            _default_intensity(t_type),
        "physical_level":       _default_physical(t_type),
        "social_level":         0.5,
        "estimated_duration":   90,
        "price_level":          2.0,
        "indoor_outdoor":       "outdoor",
        "weather_dependent":    True,
        "time_of_day_suitable": "anytime",
    }


def _default_intensity(activity_type: str) -> float:
    return {"adventure": 0.8, "relaxation": 0.1, "food": 0.2,
            "culture": 0.3, "nature": 0.5, "nightlife": 0.4, "shopping": 0.2}.get(activity_type, 0.5)

def _default_physical(activity_type: str) -> float:
    return {"adventure": 0.8, "relaxation": 0.1, "food": 0.1,
            "culture": 0.2, "nature": 0.5, "nightlife": 0.3, "shopping": 0.2}.get(activity_type, 0.3)


# =============================================================================
# DEDUPLICATION
# =============================================================================

def _deduplicate(activities: List[Dict]) -> List[Dict]:
    """
    Removes activities whose normalised names are identical.
    Preserves order (first occurrence wins — LLM output takes priority over stubs).
    """
    seen: set = set()
    unique: List[Dict] = []
    for act in activities:
        key = _normalise_name(act.get("name", ""))
        if key and key not in seen:
            seen.add(key)
            unique.append(act)
    return unique


def _normalise_name(name: str) -> str:
    """Lower-cases and strips punctuation/spaces for comparison."""
    return re.sub(r"[\s\W]+", "", name.lower())


# =============================================================================
# ID GENERATION
# =============================================================================

def _make_id(loc_id: str, index: int) -> str:
    """
    Generates a stable, unique activity ID.
    Format: act_<loc8>_<md5_6>
    Stable across runs for the same location + index.
    """
    h = hashlib.md5(f"{loc_id}_{index:04d}".encode()).hexdigest()[:6]
    prefix = loc_id[:8].lower().replace("-", "_")
    return f"act_{prefix}_{h}"


# =============================================================================
# LAZY IMPORT
# =============================================================================
import re   # noqa: E402 — placed after function definitions intentionally