# =============================================================================
# llm_generator.py
# =============================================================================
# LLM Engine for N5 Activity Generation.
# Responsibilities:
#   • Build a tight, schema-enforcing prompt (Vietnamese activities, EN schema)
#   • Call Groq with exponential-backoff retry
#   • Parse, validate, and sanitize the raw response into canonical dicts
# =============================================================================

import json
import logging
import os
import re
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional

from config.settings import GROQ_API_KEY
from backend.shared.maps.tags import ALL_TAGS

from .config import (
    GROQ_API_URL,
    GROQ_MAX_TOKENS,
    GROQ_MODEL,
    GROQ_TEMPERATURE,
    MAX_DESCRIPTION_WORDS,
    MAX_RETRIES,
    MAX_TAGS,
    MIN_TAGS,
    RETRY_BASE_DELAY_S,
    VALID_ACTIVITY_TYPES,
    VALID_INDOOR_OUTDOOR,
    VALID_TIME_OF_DAY,
)

logger = logging.getLogger("N5.LLM")

# Pre-computed for prompt injection — keep alphabetically sorted for readability
ALL_TAG_KEYS: List[str] = sorted(ALL_TAGS.keys())


# =============================================================================
# PUBLIC API
# =============================================================================

def is_llm_available() -> bool:
    return bool(GROQ_API_KEY)


def generate_activities_for_location(
    location: Dict,
    user_text: str = "",
    user_tags: List[str] = None,
    target_count: int = 10,
    templates: List[Dict] = None,
) -> List[Dict]:
    """
    Returns a list of validated activity dicts for *one* location.
    Uses templates as a hallucination-prevention ground truth.
    Each returned dict is guaranteed to pass `_validate_activity`.
    """
    if not is_llm_available():
        logger.error("Groq API key missing — cannot generate activities.")
        return []

    user_tags = user_tags or []
    templates = templates or []

    system_prompt, user_prompt = _build_prompts(
        location, user_text, user_tags, target_count, templates
    )

    logger.debug("Calling Groq (%s) for: %s", GROQ_MODEL, location["name"])
    raw_text = _call_groq(system_prompt, user_prompt)

    if not raw_text:
        logger.warning("Empty Groq response for: %s", location["name"])
        return []

    logger.debug("Groq response length: %d chars", len(raw_text))
    parsed = _extract_json(raw_text)

    if parsed is None:
        logger.error("JSON extraction failed for: %s", location["name"])
        return []

    # Normalise: accept both bare list and {"activities": [...]} wrapper
    activity_list: List[Any] = []
    if isinstance(parsed, list):
        activity_list = parsed
    elif isinstance(parsed, dict):
        for v in parsed.values():
            if isinstance(v, list):
                activity_list = v
                break

    validated = []
    for raw in activity_list:
        if not isinstance(raw, dict):
            continue
        clean = _validate_and_sanitize(raw, location["name"])
        if clean:
            validated.append(clean)

    logger.debug(
        "Validated %d / %d activities for: %s",
        len(validated), len(activity_list), location["name"]
    )
    return validated


# =============================================================================
# PROMPT BUILDER
# =============================================================================

def _build_prompts(
    loc: Dict,
    user_text: str,
    user_tags: List[str],
    target_count: int,
    templates: List[Dict],
) -> tuple[str, str]:
    """
    Returns (system_prompt, user_prompt).

    Design principles:
    - System prompt defines role + strict output contract.
    - User prompt supplies context (location, traveller, templates).
    - Description cap is enforced in both text and example.
    - Tags are given as an exhaustive allowlist — no invention permitted.
    """

    # ── System ──────────────────────────────────────────────────────────────
    system = (
        "You are an expert Vietnamese travel curator. "
        "Your ONLY output is a raw JSON array — no prose, no markdown fences, no keys outside the schema. "
        "Each description MUST be around 20 words (15–25 words): a very descriptive, vivid, and specific sentence. "
        "Never invent geography (e.g. no sea diving at a mountain). "
        "Tags MUST be chosen exclusively from the provided English-keyed ontology."
    )

    # ── Template block ───────────────────────────────────────────────────────
    if templates:
        template_lines = "\n".join(
            f"  {i+1}. {t['name']}  [{t['type']}]"
            for i, t in enumerate(templates)
        )
        template_block = (
            f"REFERENCE ACTIVITIES (use as ground truth — expand or rename freely, "
            f"but preserve the real-world essence):\n{template_lines}\n"
        )
    else:
        template_block = (
            "No reference activities provided. "
            "Generate activities that are geographically and culturally accurate for this location.\n"
        )

    # ── Tag allowlist ────────────────────────────────────────────────────────
    tag_list = ", ".join(ALL_TAG_KEYS)

    # ── Schema example (single object) ──────────────────────────────────────
    schema_example = json.dumps(
        {
            "name": "Tên hoạt động ngắn gọn",
            "description": "Một câu khoảng 20 từ, mô tả chi tiết, sống động và giàu hình ảnh về trải nghiệm.",
            "tags": ["beach", "scuba diving", "sunset", "adventure", "romantic", "vibrant"],
            "activity_type": "nature | adventure | food | culture | relaxation | nightlife | shopping",
            "activity_subtype": "hiking | snorkeling | street_food | … (free text, snake_case)",
            "intensity": 0.0,
            "physical_level": 0.0,
            "social_level": 0.0,
            "estimated_duration": 90,
            "price_level": 1.0,
            "indoor_outdoor": "indoor | outdoor | mixed",
            "weather_dependent": False,
            "time_of_day_suitable": "morning | afternoon | evening | night | anytime",
        },
        ensure_ascii=False,
        indent=2,
    )

    # ── User prompt ──────────────────────────────────────────────────────────
    traveller_line = user_text.strip() if user_text.strip() else "General traveller"
    interest_line  = ", ".join(user_tags) if user_tags else "no specific interests"

    user = f"""LOCATION: {loc['name']}
DESCRIPTION: {loc.get('description', '').strip()}

TRAVELLER PROFILE: {traveller_line}
INTERESTS: {interest_line}

{template_block}
TAG ALLOWLIST (choose {MIN_TAGS}–{MAX_TAGS} per activity):
{tag_list}

RULES:
1. Generate exactly {target_count} activities.
2. Each activity name: 4–8 Vietnamese words, vivid and specific.
3. Each description: around 20 words, very descriptive and specific, one sentence, no repetition of the name.
4. Tags: {MIN_TAGS}–{MAX_TAGS} items, ALL chosen from the ONTOLOGY allowlist above, no duplicates.
5. activity_type: one of adventure / relaxation / food / culture / nightlife / nature / shopping.
6. intensity & physical_level & social_level: float 0.0–1.0.
7. estimated_duration: integer minutes (realistic for the activity).
8. price_level: float 1.0 (free) → 4.0 (luxury).
9. indoor_outdoor: "indoor" | "outdoor" | "mixed".
10. weather_dependent: true | false.
11. time_of_day_suitable: "morning" | "afternoon" | "evening" | "night" | "anytime".
12. Do NOT repeat the same activity concept twice.

SCHEMA (each object in the array must match exactly):
{schema_example}

OUTPUT: A single JSON array of {target_count} objects. Nothing else."""

    return system, user


# =============================================================================
# GROQ API CALL
# =============================================================================

def _call_groq(system_prompt: str, user_prompt: str) -> Optional[str]:
    """
    HTTP call to Groq with exponential-backoff retry on 429.
    Returns the raw message content string, or None on failure.
    """
    payload = json.dumps(
        {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            "temperature": GROQ_TEMPERATURE,
            "max_tokens":  GROQ_MAX_TOKENS,
            "response_format": {"type": "json_object"},   # Groq JSON mode
        },
        ensure_ascii=False,
    ).encode("utf-8")

    headers = {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "User-Agent":    "N5-ActivityGen/2.0",
    }

    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(
                GROQ_API_URL, data=payload, headers=headers, method="POST"
            )
            with urllib.request.urlopen(req, timeout=90) as resp:
                result = json.loads(resp.read().decode("utf-8"))

            choices = result.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "") or None
            logger.warning("Groq returned no choices (attempt %d)", attempt + 1)
            return None

        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            if exc.code == 429:
                delay = RETRY_BASE_DELAY_S * (2 ** attempt)
                logger.warning(
                    "Groq rate-limit (429) — retry %d/%d in %.1fs",
                    attempt + 1, MAX_RETRIES, delay
                )
                time.sleep(delay)
                continue
            logger.error("Groq HTTP %d: %s", exc.code, body[:300])
            break

        except Exception as exc:
            logger.error("Groq connection error (attempt %d): %s", attempt + 1, exc)
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_BASE_DELAY_S)
            break

    return None


# =============================================================================
# JSON EXTRACTION
# =============================================================================

def _extract_json(text: str) -> Optional[Any]:
    """
    Progressively attempts to extract valid JSON from raw LLM output.
    Handles markdown fences, leading/trailing prose, and partial wrapping.
    """
    text = text.strip()

    # Strip markdown code fences
    text = re.sub(r"```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```", "", text).strip()

    # Attempt 1: direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Attempt 2: extract outermost [...] or {...}
    for open_c, close_c in (("[", "]"), ("{", "}")):
        start = text.find(open_c)
        end   = text.rfind(close_c)
        if start != -1 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                pass

    # Attempt 3: fix trailing commas (common LLM mistake) and re-parse
    fixed = re.sub(r",\s*([}\]])", r"\1", text)
    try:
        return json.loads(fixed)
    except json.JSONDecodeError:
        pass

    logger.error("All JSON extraction strategies failed.")
    return None


# =============================================================================
# VALIDATION & SANITIZATION
# =============================================================================

_VALID_TAGS_SET = set(ALL_TAG_KEYS)


def _validate_and_sanitize(raw: Dict, loc_name: str) -> Optional[Dict]:
    """
    Validates field types, clamps numeric ranges, filters invalid tags,
    truncates over-long descriptions, and fills safe defaults for missing fields.
    Returns a clean dict, or None if the activity is fundamentally unusable.
    """
    name = str(raw.get("name", "")).strip()
    if not name:
        logger.debug("Skipping activity with empty name from %s", loc_name)
        return None

    # ── Description ─────────────────────────────────────────────────────────
    description = str(raw.get("description", "")).strip()
    words = description.split()
    if len(words) > MAX_DESCRIPTION_WORDS:
        description = " ".join(words[:MAX_DESCRIPTION_WORDS]).rstrip(".,;:") + "."
        logger.debug("Truncated description for '%s' to %d words", name, MAX_DESCRIPTION_WORDS)

    # ── Tags ─────────────────────────────────────────────────────────────────
    raw_tags = raw.get("tags", [])
    if not isinstance(raw_tags, list):
        raw_tags = []
    tags = [str(t).lower().strip() for t in raw_tags if str(t).lower().strip() in _VALID_TAGS_SET]
    tags = list(dict.fromkeys(tags))          # deduplicate while preserving order
    tags = tags[:MAX_TAGS]
    if len(tags) < MIN_TAGS:
        logger.debug("Activity '%s' has only %d valid tags (min %d)", name, len(tags), MIN_TAGS)
        # Don't discard — just note. Low-tag activities still provide value.

    # ── activity_type ────────────────────────────────────────────────────────
    activity_type = str(raw.get("activity_type", "")).lower().strip()
    if activity_type not in VALID_ACTIVITY_TYPES:
        activity_type = _infer_type_from_tags(tags)

    # ── activity_subtype ─────────────────────────────────────────────────────
    activity_subtype = str(raw.get("activity_subtype", "")).lower().strip() or None

    # ── Numeric fields ───────────────────────────────────────────────────────
    intensity      = _clamp(raw.get("intensity"),      0.0, 1.0, 0.5)
    physical_level = _clamp(raw.get("physical_level"), 0.0, 1.0, 0.3)
    social_level   = _clamp(raw.get("social_level"),   0.0, 1.0, 0.5)
    duration       = _clamp(raw.get("estimated_duration"), 15, 1440, 90)
    price_level    = _clamp(raw.get("price_level"),    1.0,  4.0, 2.0)

    # ── indoor_outdoor ───────────────────────────────────────────────────────
    indoor_outdoor = str(raw.get("indoor_outdoor", "outdoor")).lower().strip()
    if indoor_outdoor not in VALID_INDOOR_OUTDOOR:
        indoor_outdoor = "outdoor"

    # ── weather_dependent ────────────────────────────────────────────────────
    weather_raw = raw.get("weather_dependent", None)
    if isinstance(weather_raw, bool):
        weather_dependent = weather_raw
    elif isinstance(weather_raw, str):
        weather_dependent = weather_raw.lower() in ("true", "1", "yes")
    else:
        # Reasonable heuristic: outdoor activities are weather-dependent by default
        weather_dependent = indoor_outdoor == "outdoor"

    # ── time_of_day_suitable ─────────────────────────────────────────────────
    tod = str(raw.get("time_of_day_suitable", "anytime")).lower().strip()
    if tod not in VALID_TIME_OF_DAY:
        tod = "anytime"

    return {
        "name":                  name,
        "description":           description,
        "tags":                  tags,
        "activity_type":         activity_type,
        "activity_subtype":      activity_subtype,
        "intensity":             round(intensity, 2),
        "physical_level":        round(physical_level, 2),
        "social_level":          round(social_level, 2),
        "estimated_duration":    int(duration),
        "price_level":           round(price_level, 1),
        "indoor_outdoor":        indoor_outdoor,
        "weather_dependent":     weather_dependent,
        "time_of_day_suitable":  tod,
    }


# =============================================================================
# INTERNAL UTILITIES
# =============================================================================

def _clamp(value: Any, lo: float, hi: float, default: float) -> float:
    try:
        v = float(value)
        return max(lo, min(hi, v))
    except (TypeError, ValueError):
        return default


_TYPE_TAG_MAP: Dict[str, str] = {
    # Maps ontology tag keys → inferred activity_type
    "trekking": "adventure", "hiking": "adventure", "motorbiking": "adventure",
    "cycling": "adventure", "rock climbing": "adventure", "caving": "adventure",
    "canyoning": "adventure", "zip lining": "adventure", "camping": "adventure",
    "scuba diving": "adventure", "snorkeling": "adventure", "kayaking": "adventure",
    "surfing": "adventure", "kitesurfing": "adventure", "rafting": "adventure",
    "spa": "relaxation", "herbal bath": "relaxation", "yoga retreat": "relaxation",
    "wellness retreat": "relaxation", "hot spring bath": "relaxation",
    "street food": "food", "local cuisine": "food", "fine dining": "food",
    "food tour": "food", "seafood": "food", "vegetarian": "food",
    "history": "culture", "war history": "culture", "colonial heritage": "culture",
    "imperial": "culture", "temple": "culture", "pagoda": "culture",
    "traditional music": "culture", "festival": "culture", "art": "culture",
    "night market": "nightlife", "rooftop bar": "nightlife", "bar": "nightlife",
    "mountain": "nature", "waterfall": "nature", "national park": "nature",
    "forest": "nature", "beach": "nature", "island": "nature",
    "shopping": "shopping", "market": "shopping",
}

def _infer_type_from_tags(tags: List[str]) -> str:
    for tag in tags:
        if tag in _TYPE_TAG_MAP:
            return _TYPE_TAG_MAP[tag]
    return "nature"  # safest default for Vietnamese destinations