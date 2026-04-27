# =============================================================================
# n5_llm_generator.py
# =============================================================================
# LLM-based activity generation sử dụng Gemini API.
#
# HYBRID APPROACH:
#   - LLM được gọi khi có GEMINI_API_KEY → sinh ~25 activities/location
#   - Mỗi location gọi LLM 1 lần với prompt yêu cầu 25 activities đa dạng
#   - Kết quả LLM + template bank = đủ 100 activities/location
#   - Fallback hoàn toàn về template nếu LLM không khả dụng
#
# THIẾT KẾ PROMPT:
#   - Yêu cầu LLM trả về JSON thuần túy, có schema cụ thể
#   - Prompt bao gồm context đầy đủ: location, user tags, constraints
#   - Chỉ dẫn rõ về sightseeing_priority (ưu tiên ngắm cảnh)
# =============================================================================

import json
import os
import re
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL   = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"

# Số activities yêu cầu LLM sinh mỗi lần gọi
LLM_ACTIVITIES_PER_CALL = 25


def is_llm_available() -> bool:
    return bool(GEMINI_API_KEY and GEMINI_API_KEY.strip())


def _build_prompt(
    location_name: str,
    location_description: str,
    location_tags: List[str],
    user_tags: List[str],
    budget_per_activity: int,
    max_time_per_activity: int,
    num_activities: int = LLM_ACTIVITIES_PER_CALL,
) -> str:
    """
    Prompt engineering cho N5:
    - Yêu cầu output JSON với đầy đủ schema theo __init__.py
    - Ưu tiên sightseeing (ngắm cảnh) vì đây là focus của hệ thống
    - Yêu cầu đa dạng activity_type và activity_subtype
    - Constraints rõ ràng: budget, time
    """
    tags_str    = ", ".join(user_tags) if user_tags else "general tourism"
    loc_tags_str = ", ".join(location_tags) if location_tags else "tourism"
    budget_str  = f"{budget_per_activity:,}".replace(",", ".")

    prompt = f"""You are an expert Vietnamese travel consultant. Generate {num_activities} diverse travel activities for tourists at the given location.

LOCATION: {location_name}
DESCRIPTION: {location_description}
LOCATION CHARACTERISTICS: {loc_tags_str}
TOURIST PREFERENCES: {tags_str}
BUDGET LIMIT PER ACTIVITY: {budget_str} VND
MAX TIME PER ACTIVITY: {max_time_per_activity} minutes

REQUIREMENTS:
1. Generate EXACTLY {num_activities} activities. No more, no less.
2. Prioritize SIGHTSEEING activities (nature viewing, panorama, sunrise/sunset, scenic spots). At least 40% of activities should be sightseeing-related.
3. Cover diverse activity types: nature, adventure, relaxation, culture, food, nightlife, shopping.
4. Each activity must be SPECIFIC and REALISTIC for {location_name}, Vietnam.
5. Respect budget ({budget_str} VND max per activity) and time ({max_time_per_activity} min max).
6. Write activity names and descriptions in Vietnamese.
7. Use English for field keys and enum values.

OUTPUT FORMAT — Return ONLY a valid JSON array, no markdown, no explanation:
[
  {{
    "name": "Tên hoạt động bằng tiếng Việt",
    "description": "Mô tả 1-2 câu bằng tiếng Việt, cụ thể cho {location_name}",
    "activity_type": "nature|adventure|relaxation|culture|food|nightlife|shopping",
    "activity_subtype": "specific subtype (e.g. sunrise_viewing, trekking, spa_massage)",
    "intensity": 0.4,
    "physical_level": 0.3,
    "social_level": 0.5,
    "estimated_duration": 120,
    "price_level": 2.0,
    "indoor_outdoor": "outdoor|indoor|mixed",
    "weather_dependent": true,
    "time_of_day_suitable": "morning|afternoon|night|anytime",
    "sightseeing_score": 0.8
  }}
]

FIELD CONSTRAINTS:
- intensity, physical_level, social_level: float 0.0–1.0
- estimated_duration: integer minutes (≤ {max_time_per_activity})
- price_level: float 1.0–5.0 (1=cheap, 5=expensive), must match budget
- sightseeing_score: float 0.0–1.0 (1.0 = pure sightseeing like panorama/sunrise)
- Make sure each activity is UNIQUE — no duplicates in name or subtype."""

    return prompt


def _parse_llm_response(response_text: str) -> Optional[List[Dict]]:
    """Parse JSON từ LLM response. Xử lý các trường hợp: pure JSON, markdown code block, JSON trong text."""
    if not response_text or not response_text.strip():
        return None

    text = response_text.strip()

    # Case 1: parse trực tiếp
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        pass

    # Case 2: markdown code block
    for pattern in [r'```json\s*\n?(.*?)\n?\s*```', r'```\s*\n?(.*?)\n?\s*```']:
        matches = re.findall(pattern, text, re.DOTALL)
        for match in matches:
            try:
                data = json.loads(match.strip())
                if isinstance(data, list):
                    return data
            except json.JSONDecodeError:
                continue

    # Case 3: tìm mảng JSON đầu tiên
    bracket_start = text.find('[')
    bracket_end   = text.rfind(']')
    if bracket_start != -1 and bracket_end > bracket_start:
        try:
            data = json.loads(text[bracket_start:bracket_end + 1])
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass

    logger.warning("Cannot parse LLM response: %s...", text[:300])
    return None


def _validate_and_normalize(act: Dict) -> Optional[Dict]:
    """
    Validate một activity từ LLM và chuẩn hóa về schema chuẩn.
    Trả về None nếu thiếu trường bắt buộc.
    """
    required = ["name", "description", "activity_type", "estimated_duration", "price_level"]
    for f in required:
        if f not in act:
            return None

    if not isinstance(act["name"], str) or not act["name"].strip():
        return None

    # Chuẩn hóa numeric fields với fallback hợp lý
    try:
        act["intensity"]          = float(act.get("intensity", 0.5))
        act["physical_level"]     = float(act.get("physical_level", 0.3))
        act["social_level"]       = float(act.get("social_level", 0.5))
        act["estimated_duration"] = int(act["estimated_duration"])
        act["price_level"]        = float(act["price_level"])
        act["sightseeing_score"]  = float(act.get("sightseeing_score", 0.3))
    except (ValueError, TypeError):
        return None

    # Clamp values to valid ranges
    act["intensity"]          = max(0.0, min(1.0, act["intensity"]))
    act["physical_level"]     = max(0.0, min(1.0, act["physical_level"]))
    act["social_level"]       = max(0.0, min(1.0, act["social_level"]))
    act["price_level"]        = max(1.0, min(5.0, act["price_level"]))
    act["sightseeing_score"]  = max(0.0, min(1.0, act["sightseeing_score"]))
    act["estimated_duration"] = max(15, act["estimated_duration"])

    # Normalize string enums
    valid_types = {"nature", "adventure", "relaxation", "culture", "food", "nightlife", "shopping"}
    if act.get("activity_type", "").lower() not in valid_types:
        act["activity_type"] = "nature"

    valid_io = {"indoor", "outdoor", "mixed"}
    if act.get("indoor_outdoor", "").lower() not in valid_io:
        act["indoor_outdoor"] = "outdoor"

    valid_tod = {"morning", "afternoon", "night", "anytime"}
    if act.get("time_of_day_suitable", "").lower() not in valid_tod:
        act["time_of_day_suitable"] = "anytime"

    act["weather_dependent"] = bool(act.get("weather_dependent", True))
    act["activity_subtype"]  = act.get("activity_subtype") or None

    return act


def call_gemini_api(prompt: str) -> Optional[str]:
    """Gọi Gemini API, trả về text response hoặc None nếu lỗi."""
    if not is_llm_available():
        return None

    import urllib.request
    import urllib.error

    url = f"{GEMINI_API_URL}/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.8,
            "topP": 0.9,
            "maxOutputTokens": 8192,  # Đủ cho 25 activities JSON
        },
    }

    try:
        data = json.dumps(payload).encode("utf-8")
        req  = urllib.request.Request(
            url, data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=45) as resp:
            result = json.loads(resp.read().decode("utf-8"))

        candidates = result.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                return parts[0].get("text", "")

        logger.warning("Gemini unexpected response format: %s", str(result)[:200])
        return None

    except Exception as e:
        logger.error("Gemini API error: %s", e)
        return None


def generate_from_llm(
    location_name: str,
    location_description: str,
    location_tags: List[str],
    user_tags: List[str],
    budget_per_activity: int,
    max_time_per_activity: int,
    num_activities: int = LLM_ACTIVITIES_PER_CALL,
) -> Optional[List[Dict]]:
    """
    Sinh activities từ LLM (Gemini).
    
    Returns:
        List[Dict] đã validate nếu thành công.
        None nếu LLM không khả dụng hoặc thất bại.
    """
    if not is_llm_available():
        return None

    prompt = _build_prompt(
        location_name=location_name,
        location_description=location_description,
        location_tags=location_tags,
        user_tags=user_tags,
        budget_per_activity=budget_per_activity,
        max_time_per_activity=max_time_per_activity,
        num_activities=num_activities,
    )

    logger.info("Calling Gemini for location: %s (requesting %d activities)", location_name, num_activities)
    response_text = call_gemini_api(prompt)

    if response_text is None:
        logger.warning("Gemini returned no response for %s", location_name)
        return None

    raw_list = _parse_llm_response(response_text)
    if raw_list is None:
        logger.warning("Failed to parse Gemini response for %s", location_name)
        return None

    valid = []
    for act in raw_list:
        normalized = _validate_and_normalize(act)
        if normalized:
            valid.append(normalized)
        else:
            logger.debug("Dropped invalid LLM activity: %s", act.get("name", "?"))

    if not valid:
        logger.warning("No valid activities from LLM for %s", location_name)
        return None

    logger.info("LLM generated %d valid activities for %s", len(valid), location_name)
    return valid