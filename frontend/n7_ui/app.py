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

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG — wide so output sections use full screen
# ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Travel Planner", page_icon="🧭", layout="wide")


# ─────────────────────────────
# QUESTIONNAIRE DATA
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


# ═════════════════════════════════════════════════════════════
# INPUT SECTION — centered via columns [1, 2, 1]
# ═════════════════════════════════════════════════════════════

_, col_input, _ = st.columns([1, 2, 1])

with col_input:
    st.title("🧭 Travel Planner")
    st.markdown("Answer a few questions and we'll find your perfect destination.")

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
        # getvalue() trả về toàn bộ bytes bất kể vị trí file pointer sau Image.open()
        image_b64 = base64.b64encode(uploaded_image.getvalue()).decode("utf-8")

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

    submit = st.button("🚀 Tìm kiếm địa điểm", use_container_width=True)


# ═════════════════════════════════════════════════════════════
# OUTPUT SECTION — full wide page
# ═════════════════════════════════════════════════════════════

if submit:

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
                timeout=60
            )

            if res.status_code != 200:
                st.error(res.text)
                st.stop()

            data = res.json()
            locations = data.get("locations", [])
            trace = data.get("trace", {})
            user_trace = trace.get("user", {})
            user_vectors = user_trace.get("user_vectors", {})
            sig_k = user_trace.get("n1_embedding", {}).get("sig_k", 0)
            img_desc = user_trace.get("n2_image", {}).get("img_desc", "")

            st.success("✅ Tìm thấy kết quả!")
            st.subheader("📍 Địa điểm gợi ý")

            # ─────────────────────────────────────────────
            # STEP 1: Render ALL locations with activity placeholders
            # ─────────────────────────────────────────────
            placeholders = []  # collect (placeholder, loc_id, meta)

            for loc in locations:
                loc_id = loc.get("location_id", "unknown")
                meta = loc.get("metadata", {})
                name = meta.get("name", loc_id)
                score = loc.get("score", 0)
                reason = loc.get("reason", "")
                desc = meta.get("description", "")
                img_path = loc.get("image_path", "")

                # 2-column row: location | activities  (1:1 ratio)
                col_loc, col_act = st.columns(2)

                with col_loc:
                    st.markdown(f"### {name}")
                    st.metric("Score", f"{score:.4f}")
                    if reason:
                        st.caption(f"💡 {reason}")
                    if desc:
                        st.write(desc)
                    if img_path:
                        try:
                            st.image(img_path, caption=name, use_container_width=True)
                        except Exception:
                            pass

                with col_act:
                    st.markdown("#### 🎯 Activities")
                    ph = st.empty()
                    with ph.container():
                        st.caption("⏳ Loading activities…")

                    placeholders.append({
                        "placeholder": ph,
                        "loc_id": loc_id,
                        "meta": meta,
                    })

                st.divider()

            # ─────────────────────────────────────────────
            # STEP 2: Stream activities into each placeholder
            # ─────────────────────────────────────────────
            for item in placeholders:
                ph = item["placeholder"]
                loc_id = item["loc_id"]
                meta = item["meta"]

                # show "generating…" state
                with ph.container():
                    st.caption(f"🔄 Generating activities for **{meta.get('name', loc_id)}**…")

                act_payload = {
                    "text": user_text,
                    "img_desc": img_desc,
                    "tags": tags,
                    "sig_k": sig_k,
                    "user_vectors": user_vectors,
                    "constraints": {},
                    "context": {},
                    "location": {"location_id": loc_id, "metadata": meta},
                    "top_k_activities": 5,
                }

                try:
                    act_res = requests.post(
                        "http://localhost:5000/activities",
                        json=act_payload,
                        timeout=120,
                    )
                    if act_res.status_code == 200:
                        ranked_activities = act_res.json().get("activities", [])

                        with ph.container():
                            if not ranked_activities:
                                st.write("No activities found.")
                            for act in ranked_activities:
                                a_meta = act.get("metadata", {})
                                a_name = a_meta.get("name", "Unknown")
                                a_score = act.get("score", 0)
                                a_reason = act.get("reason", "")
                                a_type = a_meta.get("activity_type", "")

                                st.markdown(
                                    f"**{a_name}** ({a_type})  \n"
                                    f"Score: `{a_score:.2f}` — {a_reason}"
                                )
                    else:
                        with ph.container():
                            st.error("Failed to load activities.")
                except Exception as e:
                    with ph.container():
                        st.error(f"Error: {e}")

            # ─── TRACE (DEBUG) ───
            with st.expander("🔍 Trace (Debug)"):
                st.markdown("**User Input**")
                st.json(user_trace.get("input", {}))

                n2_trace = user_trace.get("n2_image", {})
                if n2_trace.get("img_desc"):
                    st.markdown("**N2 — Image Description**")
                    st.write(n2_trace["img_desc"])

                n1_trace = user_trace.get("n1_embedding", {})
                st.markdown(f"**N1 — sig_k = {n1_trace.get('sig_k', '?')}**")

                st.markdown("**Vector Dimensions**")
                st.json(user_trace.get("vector_dims", {}))

                st.markdown("**N4 — Ranking**")
                st.json(trace.get("ranking", {}))

                st.markdown("**Debug**")
                st.json(trace.get("debug", {}))

            with st.expander("📦 RAW RESPONSE"):
                st.json(data)

        except Exception as e:
            st.error(f"Connection failed: {e}")
