"""
N7 — Travel Questionnaire UI (Streamlit)

7 questions → 8–14 tags from ALL_TAGS ontology → N8 API
Follows tagging-guide.md rules:
  - Each answer maps to 1–2 actual ALL_TAGS keys
  - Activities get the most tag budget (2–3 tags)
  - Vibe is the tie-breaker (1–2 tags)
  - Total user tags: 8–14, never exceed 20
"""

import streamlit as st
import requests
from PIL import Image
import base64

st.set_page_config(page_title="Travel Planner", page_icon="🧭", layout="centered")

st.title("🧭 Travel Planner")
st.markdown("Answer a few questions and we'll find your perfect destination.")

# ─────────────────────────────
# QUESTIONNAIRE
# ─────────────────────────────
# Each option value is a list of EXACT ALL_TAGS keys.
# Budget: 1–2 tags per question, ~8–14 total.

QUESTIONS = [

    # ─────────────────────────────
    # Q1 — TERRAIN / WATER (→ 1–2 tags)
    # ─────────────────────────────
    {
        "q": "🏔️ What landscape do you prefer?",
        "type": "radio",
        "tags": {
            "Beach & Coast":    ["beach", "island"],
            "Mountains":        ["mountain"],
            "Countryside":      ["rice terrace", "valley"],
            "River & Delta":    ["river", "delta"],
            "Forest & Nature":  ["forest", "national park"],
            "City":             ["city"],
        }
    },

    # ─────────────────────────────
    # Q2 — ACTIVITIES (→ 2–3 tags) ← highest budget
    # ─────────────────────────────
    {
        "q": "🎯 What activities interest you? (pick up to 3)",
        "type": "multi",
        "max": 3,
        "tags": {
            "Trekking / Hiking":   ["trekking"],
            "Snorkeling / Diving": ["snorkeling"],
            "Kayaking":            ["kayaking"],
            "Cycling":             ["cycling"],
            "Motorbiking":         ["motorbiking"],
            "Camping":             ["camping"],
            "Boat Cruise":         ["boat cruise"],
            "Photography":         ["photography"],
            "Cooking Class":       ["cooking class"],
            "Spa & Wellness":      ["spa"],
            "Sightseeing":         ["sightseeing"],
            "Surfing":             ["surfing"],
        }
    },

    # ─────────────────────────────
    # Q3 — VIBE / MOOD (→ 1–2 tags) ← tie-breaker
    # ─────────────────────────────
    {
        "q": "✨ What vibe are you after? (pick up to 2)",
        "type": "multi",
        "max": 2,
        "tags": {
            "Peaceful & Quiet":     ["peaceful"],
            "Adventurous & Wild":   ["adventure"],
            "Romantic & Intimate":  ["romantic"],
            "Vibrant & Lively":     ["vibrant"],
            "Off the Beaten Path":  ["off the beaten path"],
            "Instagrammable":       ["instagrammable"],
            "Cozy & Warm":          ["cozy"],
            "Authentic & Local":    ["authentic"],
        }
    },

    # ─────────────────────────────
    # Q4 — COMPANION (→ 1 tag)
    # ─────────────────────────────
    {
        "q": "👥 Who are you traveling with?",
        "type": "radio",
        "tags": {
            "Solo":             ["solo"],
            "Couple":           ["couple"],
            "Family":           ["family"],
            "Friends":          ["friends trip"],
            "Group / Team":     ["group"],
        }
    },

    # ─────────────────────────────
    # Q5 — DURATION (→ 1 tag)
    # ─────────────────────────────
    {
        "q": "📅 How long is your trip?",
        "type": "radio",
        "tags": {
            "Day trip":         ["day trip"],
            "Weekend (2–3 days)": ["weekend trip"],
            "1 week+":          ["long stay"],
        }
    },

    # ─────────────────────────────
    # Q6 — BUDGET (→ 1 tag)
    # ─────────────────────────────
    {
        "q": "💰 What's your budget style?",
        "type": "radio",
        "tags": {
            "Budget / Backpacker": ["budget"],
            "Mid-range":           ["mid range"],
            "Luxury":              ["luxury"],
            "Homestay / Eco":      ["homestay"],
        }
    },

    # ─────────────────────────────
    # Q7 — FOOD (→ 0–1 tag)
    # ─────────────────────────────
    {
        "q": "🍜 Any food preferences?",
        "type": "radio",
        "tags": {
            "Street food":      ["street food"],
            "Seafood":          ["seafood"],
            "Local cuisine":    ["local cuisine"],
            "Fine dining":      ["fine dining"],
            "No preference":    [],
        }
    },
]


# ─────────────────────────────
# FREE TEXT + IMAGE
# ─────────────────────────────

st.divider()

user_text = st.text_area("✍️ Describe your ideal trip (optional)",
                         placeholder="E.g. I want a relaxing beach getaway with great seafood...")

uploaded_image = st.file_uploader("🖼 Upload inspiration image (optional)", type=["png", "jpg", "jpeg"])

image_b64 = ""

if uploaded_image:
    img = Image.open(uploaded_image)
    st.image(img, caption="Uploaded Image")

    # encode image for backend (N2)
    uploaded_image.seek(0)
    image_b64 = base64.b64encode(uploaded_image.read()).decode("utf-8")

# ─────────────────────────────
# QUESTIONS ENGINE
# ─────────────────────────────

st.divider()

tags = []

for i, item in enumerate(QUESTIONS):
    st.subheader(item["q"])

    if item["type"] == "radio":
        ans = st.radio("", list(item["tags"].keys()), key=f"q{i}", label_visibility="collapsed")
        tags += item["tags"].get(ans, [])

    elif item["type"] == "multi":
        max_sel = item.get("max", 3)
        ans = st.multiselect("", list(item["tags"].keys()), key=f"q{i}",
                             max_selections=max_sel, label_visibility="collapsed")
        for a in ans:
            tags += item["tags"].get(a, [])

    st.divider()

# remove duplicates, preserve order
seen = set()
tags = [t for t in tags if t not in seen and not seen.add(t)]

# Show tag summary
st.caption(f"🏷️ Tags selected: {len(tags)} — {', '.join(tags) if tags else 'none'}")

# ─────────────────────────────
# SUBMIT
# ─────────────────────────────

if st.button("🚀 Tìm kiếm địa điểm", use_container_width=True):

    if not user_text and not tags:
        st.warning("Please answer at least one question or describe your trip.")
    else:
        # N8 API contract: { text, image, tags, constraints, top_k_locations }
        payload = {
            "text": user_text,
            "image": image_b64,
            "tags": tags,
            "constraints": {},
            "top_k_locations": 5,
        }

        st.info(f"📝 text: {len(user_text)} chars | 🏷️ tags: {len(tags)} | 🖼️ image: {'yes' if image_b64 else 'no'}")

        try:
            res = requests.post(
                "http://localhost:5000/recommend",
                json=payload,
                timeout=30
            )

            if res.status_code == 200:
                data = res.json()

                st.success("✅ Tìm thấy kết quả!")

                # ─── LOCATIONS ───
                st.subheader("📍 Địa điểm gợi ý")
                for loc in data.get("locations", []):
                    meta = loc.get("metadata", {})
                    name = meta.get("name", loc.get("location_id", "Unknown"))
                    score = loc.get("score", 0)
                    reason = loc.get("reason", "")
                    desc = meta.get("description", "")

                    st.markdown(f"### {name}")
                    st.metric("Score", f"{score:.4f}")
                    if reason:
                        st.caption(f"💡 {reason}")
                    if desc:
                        st.write(desc)

                    # Show image if available
                    img_path = loc.get("image_path", "")
                    if img_path:
                        try:
                            st.image(img_path, caption=name)
                        except Exception:
                            pass

                    st.divider()

                # ─── TRACE (DEBUG) ───
                with st.expander("🔍 Trace (Debug)"):
                    trace = data.get("trace", {})

                    # User input
                    st.markdown("**User Input**")
                    user_trace = trace.get("user", {})
                    st.json(user_trace.get("input", {}))

                    # N2 image
                    n2_trace = user_trace.get("n2_image", {})
                    if n2_trace.get("img_desc"):
                        st.markdown("**N2 — Image Description**")
                        st.write(n2_trace["img_desc"])

                    # N1 embedding
                    n1_trace = user_trace.get("n1_embedding", {})
                    st.markdown(f"**N1 — sig_k = {n1_trace.get('sig_k', '?')}**")

                    # Vector dims
                    st.markdown("**Vector Dimensions**")
                    st.json(user_trace.get("vector_dims", {}))

                    # Ranking
                    st.markdown("**N4 — Ranking**")
                    st.json(trace.get("ranking", {}))

                    # Debug
                    st.markdown("**Debug**")
                    st.json(trace.get("debug", {}))

                with st.expander("📦 RAW RESPONSE"):
                    st.json(data)

            else:
                st.error(res.text)

        except Exception as e:
            st.error(f"Connection failed: {e}")