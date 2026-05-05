"""
views/result/__init__.py
"""
import streamlit as st
from .api import fetch_activities

_DEFAULT_SHOW = 5


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

    # ── Input Summary Section ──
    with st.container(border=True):
        st.markdown("**📋 Thông tin tìm kiếm của bạn:**")

        if tags:
            badges = "".join(f'<span class="tag-badge">{t}</span> ' for t in tags)
            st.markdown(
                f'<div style="margin-bottom: 8px;">{badges}</div>',
                unsafe_allow_html=True,
            )

        summary_cols = st.columns([3, 1] if image_b64 else [1])

        with summary_cols[0]:
            if user_text:
                st.markdown(f"> *\"{user_text}\"*")
            elif not tags and not image_b64:
                st.markdown("> *Không có văn bản mô tả*")

        if image_b64 and len(summary_cols) > 1:
            with summary_cols[1]:
                st.markdown(
                    """
                    <div style="background-color:#21262d; border:1px solid #30363d;
                    border-radius:4px; padding:6px 12px; text-align:center; font-size:0.85rem;">
                        📷 Đã gửi hình ảnh
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
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

    placeholders: list[dict] = []

    for loc in locations:
        loc_id: str = loc.get("location_id", "unknown")
        meta: dict = loc.get("metadata", {})
        ph = _render_location_card(loc)
        placeholders.append({"ph": ph, "loc_id": loc_id, "meta": meta})
        st.divider()

    for item in placeholders:
        loc_id = item["loc_id"]
        meta = item["meta"]
        ph = item["ph"]

        if loc_id in st.session_state.activity_results:
            _render_activities(ph, st.session_state.activity_results[loc_id], loc_id)
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
    loc_id: str,
) -> None:
    """Render up to 5 activities per filter by default, with a show-more toggle."""
    if not activities:
        with placeholder.container():
            st.caption("Không có hoạt động nào được gợi ý.")
        return

    all_types = sorted(
        {a.get("metadata", {}).get("activity_type", "") for a in activities} - {""}
    )

    # Per-location show-more state key
    show_all_key = f"show_all_{loc_id}"
    if show_all_key not in st.session_state:
        st.session_state[show_all_key] = False

    with placeholder.container():
        if all_types:
            selected_type = st.selectbox(
                "Lọc theo loại",
                options=["Tất cả"] + all_types,
                key=f"filter_{loc_id}",
                label_visibility="collapsed",
            )
            # Reset show-more when filter changes
            filter_key = f"filter_{loc_id}_prev"
            if st.session_state.get(filter_key) != selected_type:
                st.session_state[show_all_key] = False
                st.session_state[filter_key] = selected_type
        else:
            selected_type = "Tất cả"

        # Filter activities
        filtered = [
            a for a in activities
            if selected_type == "Tất cả"
            or a.get("metadata", {}).get("activity_type", "") == selected_type
        ]

        visible = filtered if st.session_state[show_all_key] else filtered[:_DEFAULT_SHOW]

        for act in visible:
            a_meta = act.get("metadata", {})
            a_type = a_meta.get("activity_type", "")
            a_name = a_meta.get("name", "Unknown")
            a_score = act.get("score", 0)
            a_reason = act.get("reason", "")
            with st.container(border=True):
                label = f"**{a_name}**"
                if a_type:
                    label += f" `{a_type}`"
                st.markdown(label)
                st.caption(f"Điểm: {a_score:.2f} — {a_reason}")

        # Show more / show less toggle
        if len(filtered) > _DEFAULT_SHOW:
            hidden = len(filtered) - _DEFAULT_SHOW
            if not st.session_state[show_all_key]:
                if st.button(
                    f"Xem thêm {hidden} hoạt động ▾",
                    key=f"more_{loc_id}_{selected_type}",
                    use_container_width=True,
                ):
                    st.session_state[show_all_key] = True
                    st.rerun()
            else:
                if st.button(
                    "Thu gọn ▴",
                    key=f"less_{loc_id}_{selected_type}",
                    use_container_width=True,
                ):
                    st.session_state[show_all_key] = False
                    st.rerun()