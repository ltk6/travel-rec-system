"""
views/result/__init__.py
"""
import streamlit as st
from .api import fetch_activities


def render_result_view(data: dict) -> None:
    if "activity_results" not in st.session_state:
        st.session_state.activity_results = {}

    locations: list = data.get("locations", [])
    trace: dict = data.get("trace", {})
    user_trace: dict = trace.get("user", {})
    user_input: dict = user_trace.get("input", {})

    user_vectors: dict = user_trace.get("user_vectors", {})
    sig_k: float = user_trace.get("n1_embedding", {}).get("sig_k", 0)
    img_desc: str = user_trace.get("n2_image", {}).get("img_desc", "")
    user_text: str = user_input.get("text", "")
    tags: list = user_input.get("tags", [])
    image_b64: str = user_input.get("image", "")

    # ── Header ──
    st.success(f"✅ Tìm thấy {len(locations)} địa điểm phù hợp")

    # ── Input Summary Section (Persistent metadata display) ──
    with st.container(border=True):
        st.markdown("**📋 Thông tin tìm kiếm của bạn:**")
        
        # Display tags if present
        if tags:
            badges = "".join(f'<span class="tag-badge">{t}</span> ' for t in tags)
            st.markdown(
                f'<div style="margin-bottom: 8px;">{badges}</div>',
                unsafe_allow_html=True,
            )

        # Build combined text and image info
        summary_cols = st.columns([3, 1] if image_b64 else [1])
        
        with summary_cols[0]:
            if user_text:
                st.markdown(f"> *\"{user_text}\"*")
            elif not tags and not image_b64:
                st.markdown("> *Không có văn bản mô tả*")

        if image_b64 and len(summary_cols) > 1:
            with summary_cols[1]:
                # Render an interactive visual anchor for the attached image
                st.markdown(
                    """
                    <div style="background-color:#21262d; border:1px solid #30363d; 
                    border-radius:4px; padding:6px 12px; text-align:center; font-size:0.85rem;">
                        📷 Đã gửi hình ảnh
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                # Expandable image preview
                with st.popover("Xem ảnh", use_container_width=True):
                    try:
                        st.image(f"data:image/jpeg;base64,{image_b64}", use_container_width=True)
                    except Exception:
                        st.caption("Không thể hiển thị hình ảnh")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📍 Địa điểm gợi ý")

    if not locations:
        st.info("Không tìm thấy địa điểm nào phù hợp. Hãy thử lại với thông tin khác.")
        return

    # ── Render each location + queue activity fetching ──
    placeholders: list[dict] = []

    for loc in locations:
        loc_id: str = loc.get("location_id", "unknown")
        meta: dict = loc.get("metadata", {})
        ph = _render_location_card(loc)
        placeholders.append({"ph": ph, "loc_id": loc_id, "meta": meta})
        st.divider()

    # ── Fill activity placeholders ──
    for item in placeholders:
        loc_id = item["loc_id"]
        meta = item["meta"]
        ph = item["ph"]

        if loc_id in st.session_state.activity_results:
            _render_activities(ph, st.session_state.activity_results[loc_id])
            continue

        with ph.container():
            st.caption(f"🔄 Đang tìm hoạt động tại **{meta.get('name', loc_id)}**…")

        try:
            activities = fetch_activities(
                loc_id=loc_id,
                meta=meta,
                user_text=user_text,
                img_desc=img_desc,
                tags=tags,
                sig_k=sig_k,
                user_vectors=user_vectors,
            )
            st.session_state.activity_results[loc_id] = activities
            st.rerun()
        except Exception as exc:
            with ph.container():
                st.error(f"Không tải được hoạt động: {exc}")
        return


# ─── Helpers ─────────────────────────────────────────────────────────────────


def _render_location_card(loc: dict) -> st.delta_generator.DeltaGenerator:
    """Render the left column (location info) and return the right column placeholder."""
    loc_id: str = loc.get("location_id", "unknown")
    meta: dict = loc.get("metadata", {})
    name: str = meta.get("name", loc_id)
    score: float = loc.get("score", 0)
    reason: str = loc.get("reason", "")
    desc: str = meta.get("description", "")
    img_path: str = loc.get("image_path", "")

    col_loc, col_act = st.columns(2, gap="large")

    with col_loc:
        st.markdown(f"### {name}")
        st.metric("Điểm phù hợp", f"{score:.4f}")
        if reason:
            st.info(f"💡 {reason}")
        if desc:
            st.write(desc)
        if img_path:
            try:
                st.image(img_path, caption=name, use_container_width=True)
            except Exception:
                st.caption("🖼️ Hình ảnh không khả dụng")

    with col_act:
        with st.container(border=True):
            st.markdown("#### 🎯 Hoạt động tại đây")
            placeholder = st.empty()
            with placeholder.container():
                st.caption("⏳ Đang tải…")

    return placeholder


def _render_activities(
    placeholder: st.delta_generator.DeltaGenerator,
    activities: list,
) -> None:
    """Fill a placeholder with a rendered activity list, with optional type filter."""
    if not activities:
        with placeholder.container():
            st.caption("Không có hoạt động nào được gợi ý.")
        return

    all_types = sorted(
        {a.get("metadata", {}).get("activity_type", "") for a in activities}
        - {""}
    )

    with placeholder.container():
        if all_types:
            selected_type = st.selectbox(
                "Lọc theo loại",
                options=["Tất cả"] + all_types,
                key=f"filter_{id(activities)}",
                label_visibility="collapsed",
            )
        else:
            selected_type = "Tất cả"

        for act in activities:
            a_meta = act.get("metadata", {})
            a_type = a_meta.get("activity_type", "")
            if selected_type != "Tất cả" and a_type != selected_type:
                continue
            a_name = a_meta.get("name", "Unknown")
            a_score = act.get("score", 0)
            a_reason = act.get("reason", "")
            with st.container(border=True):
                label = f"**{a_name}**"
                if a_type:
                    label += f" `{a_type}`"
                st.markdown(label)
                st.caption(f"Điểm: {a_score:.2f} — {a_reason}")
