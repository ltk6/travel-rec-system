# =============================================================================
# config.py
# =============================================================================
# Single source of truth for all N5 Activity Generation tunables.
# All values can be overridden via environment variables.
# =============================================================================

import os

# ---------------------------------------------------------------------------
# Generation Targets
# ---------------------------------------------------------------------------
DEFAULT_TARGET_PER_LOCATION = int(os.getenv("N5_TARGET_PER_LOC", 10))
MAX_TARGET_PER_LOCATION     = int(os.getenv("N5_MAX_TARGET", 20))

# ---------------------------------------------------------------------------
# LLM Backend
# ---------------------------------------------------------------------------
# llama-3.3-70b-versatile gives far better structured output than 8b-instant.
# Switch back to 8b if Groq TPM is tight.
GROQ_MODEL   = os.getenv("N5_GROQ_MODEL", "meta-llama/Llama-4-Scout-17B-16E-Instruct")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_TEMPERATURE = float(os.getenv("N5_TEMPERATURE", 0.45))   # lower = tighter schema adherence
GROQ_MAX_TOKENS  = int(os.getenv("N5_MAX_TOKENS", 4096))

# ---------------------------------------------------------------------------
# LLM Ratio
# ---------------------------------------------------------------------------
# 1.0  → 100 % LLM-generated (templates used only as reference hints)
# 0.5  → 50 % from templates verbatim + 50 % LLM expansion
# Currently always 1.0; kept here so the generator can apply it.
LLM_RATIO = float(os.getenv("N5_LLM_RATIO", 1.0))

# ---------------------------------------------------------------------------
# Retry & Rate-Limit Handling
# ---------------------------------------------------------------------------
MAX_RETRIES          = int(os.getenv("N5_MAX_RETRIES", 5))
RETRY_BASE_DELAY_S   = float(os.getenv("N5_RETRY_BASE_DELAY", 4.0))   # doubles per attempt
INTER_REQUEST_DELAY_S = float(os.getenv("N5_INTER_REQUEST_DELAY", 1.5))

# ---------------------------------------------------------------------------
# Embedding-Quality Constraints
# ---------------------------------------------------------------------------
# Short, dense descriptions embed better and cost fewer tokens downstream.
MAX_DESCRIPTION_WORDS = int(os.getenv("N5_MAX_DESC_WORDS", 30))

# Tag cardinality per activity
MIN_TAGS = int(os.getenv("N5_MIN_TAGS", 6))
MAX_TAGS = int(os.getenv("N5_MAX_TAGS", 10))

# ---------------------------------------------------------------------------
# Valid Activity Types  (canonical; used for validation fallback)
# ---------------------------------------------------------------------------
VALID_ACTIVITY_TYPES = {
    "adventure", "relaxation", "food", "culture",
    "nightlife", "nature", "shopping"
}

VALID_INDOOR_OUTDOOR = {"indoor", "outdoor", "mixed"}
VALID_TIME_OF_DAY    = {"morning", "afternoon", "evening", "night", "anytime"}