import streamlit as st
import requests
from PIL import Image
import base64

st.set_page_config(page_title="Travel Questionnaire", page_icon="🧭", layout="centered")

st.title("🧭 Travel Questionnaire")
st.markdown("20 questions + text + image → structured output for N1")

# ─────────────────────────────
# QUESTIONS
# ─────────────────────────────
QUESTIONS = [

    # ─────────────────────────────
    # Q1 — SOCIAL
    # ─────────────────────────────
    {
        "q": "Q1. Who is coming?",
        "type": "radio",
        "options": {
            "Solo": ["solo", "independent", "flexible", "quiet", "self-paced", "free"],
            "Couple": ["couple", "romantic", "intimate", "private", "together", "love"],
            "Family": ["family", "kids", "safe", "stable", "comfortable", "easy"],
            "Friends": ["group", "social", "lively", "fun", "shared", "active"]
        }
    },

    # ─────────────────────────────
    # Q2 — DURATION
    # ─────────────────────────────
    {
        "q": "Q2. Duration?",
        "type": "radio",
        "options": {
            "1 day": ["short", "quick", "fast", "near", "simple", "light"],
            "2–3 days": ["weekend", "balanced", "mid", "flexible", "short-trip", "easy"],
            "1 week+": ["long", "deep", "slow", "extended", "immersive", "full"]
        }
    },

    # ─────────────────────────────
    # Q3 — DISTANCE
    # ─────────────────────────────
    {
        "q": "Q3. Distance?",
        "type": "radio",
        "options": {
            "Near": ["near", "local", "short-travel", "quick", "easy", "low-effort"],
            "Domestic": ["domestic", "country", "regional", "accessible", "standard", "varied"],
            "International": ["intl", "global", "far", "long", "diverse", "new"]
        }
    },

    # ─────────────────────────────
    # Q4 — MOTIVATION
    # ─────────────────────────────
    {
        "q": "Q4. Why travel?",
        "type": "radio",
        "options": {
            "Rest": ["relax", "peace", "calm", "slow", "reset", "quiet"],
            "Adventure": ["adventure", "explore", "active", "challenge", "movement", "excitement"],
            "Culture": ["culture", "heritage", "local", "history", "learning", "city"],
            "Romance": ["romantic", "love", "couple", "intimate", "private", "emotion"]
        }
    },

    # ─────────────────────────────
    # Q5 — ENVIRONMENT (CRITICAL)
    # ─────────────────────────────
    {
        "q": "Q5. Environment?",
        "type": "radio",
        "options": {
            "Beach": ["beach", "sea", "coastal", "sun", "island", "waves"],
            "Mountain": ["mountain", "highland", "cool", "elevation", "hiking", "nature"],
            "City": ["city", "urban", "modern", "buildings", "nightlife", "busy"],
            "Nature": ["nature", "forest", "wild", "green", "fresh", "eco"],
            "Resort": ["resort", "luxury", "comfort", "spa", "service", "relax"]
        }
    },

    # ─────────────────────────────
    # Q6 — CULTURE LEVEL
    {
        "q": "Q6. Culture level?",
        "type": "radio",
        "options": {
            "High": ["culture", "heritage", "history", "local", "deep", "tradition"],
            "Mid": ["culture-lite", "light", "mixed", "casual", "some", "balanced"],
            "Low": ["minimal", "none", "nature", "relax", "simple", "non-cultural"]
        }
    },

    # ─────────────────────────────
    # Q7 — CULTURE FOCUS
    {
        "q": "Q7. Cultural focus",
        "type": "multi",
        "options": {
            "Food": ["food", "eat", "local", "street", "taste", "cuisine"],
            "Temples": ["temple", "spiritual", "religion", "sacred", "heritage", "calm"],
            "Markets": ["market", "street", "local", "shopping", "culture", "busy"],
            "Art": ["art", "museum", "creative", "design", "culture", "visual"]
        }
    },

    # ─────────────────────────────
    # Q8 — ACTIVITY
    {
        "q": "Q8. Activity level?",
        "type": "radio",
        "options": {
            "Active": ["active", "move", "sport", "outdoor", "energy", "adventure"],
            "Moderate": ["balanced", "mid", "walk", "flexible", "normal", "steady"],
            "Relaxed": ["relax", "slow", "rest", "calm", "easy", "low-energy"]
        }
    },

    # ─────────────────────────────
    # Q9 — ACTIVITIES
    {
        "q": "Q9. Activities",
        "type": "multi",
        "options": {
            "Hiking": ["hiking", "trek", "mountain", "outdoor", "nature", "climb"],
            "Swimming": ["swim", "water", "beach", "sea", "cool", "refresh"],
            "Camping": ["camp", "night", "outdoor", "nature", "sleep", "wild"],
            "Photo": ["photo", "view", "scenic", "capture", "aesthetic", "frame"]
        }
    },

    # ─────────────────────────────
    # Q10 — VIBE
    {
        "q": "Q10. Vibe",
        "type": "multi",
        "options": {
            "Quiet": ["quiet", "peace", "calm", "silent", "relax", "soft"],
            "Lively": ["lively", "fun", "energy", "busy", "social", "vibrant"],
            "Romantic": ["romantic", "love", "couple", "intimate", "warm", "soft"],
            "Photo": ["photo", "aesthetic", "instagram", "view", "scenic", "visual"]
        }
    }
]

# ─────────────────────────────
# GLOBAL INPUTS
# ─────────────────────────────

st.divider()

user_text = st.text_area("✍️ Describe your ideal trip (optional)")

uploaded_image = st.file_uploader("🖼 Upload image (optional)", type=["png", "jpg", "jpeg"])

image_description = ""
image_b64 = ""

if uploaded_image:
    img = Image.open(uploaded_image)
    st.image(img, caption="Uploaded Image")

    # encode image for backend
    image_b64 = base64.b64encode(uploaded_image.read()).decode("utf-8")
    image_description = "user_uploaded_image"

# ─────────────────────────────
# QUESTIONS ENGINE
# ─────────────────────────────

tags = []
answers = {}

for i, item in enumerate(QUESTIONS):
    st.subheader(item["q"])

    if item["type"] == "radio":
        ans = st.radio("", list(item["options"].keys()), key=f"q{i}")
        tags += item["options"].get(ans, [])
        answers[item["q"]] = ans

    elif item["type"] == "multi":
        ans = st.multiselect("", list(item["options"].keys()), key=f"q{i}")
        for a in ans:
            tags += item["options"].get(a, [])
        answers[item["q"]] = ans

    st.divider()

# remove duplicates
tags = list(set(tags))

# ─────────────────────────────
# SUBMIT
# ─────────────────────────────

if st.button("🚀 Tìm kiếm lộ trình", use_container_width=True):

    payload = {
        "text": user_text,
        "image_description": image_description,
        "image": image_b64,
        "tags": tags,
        "answers": answers
    }

    st.write("📦 DEBUG payload:", payload)

    try:
        res = requests.post(
            "http://localhost:5000/recommend",
            json=payload,
            timeout=15
        )

        st.write("📡 Status:", res.status_code)

        if res.status_code == 200:
            data = res.json()

            st.success("✅ Success")

            with st.expander("RAW RESPONSE"):
                st.json(data)

            st.subheader("📍 Locations")
            for loc in data.get("locations", []):
                meta = loc.get("metadata", {})
                st.markdown(f"### {meta.get('name', loc.get('location_id'))}")
                st.write(loc.get("score", 0))
                st.write(meta.get("description", ""))

            st.subheader("🎯 Activities")
            for act in data.get("activities", []):
                st.write(f"- {act.get('activity_id')} ({act.get('score', 0):.3f})")

        else:
            st.error(res.text)

    except Exception as e:
        st.error(f"Connection failed: {e}")