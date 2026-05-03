"""
questionnaire.py — Renders travel preferences with complete progress and state persistence.
"""
import streamlit as st
from .questionnaire_data import QUESTIONNAIRE_CONFIG, EMOJI_MAP

# ─── Public Entry Point ──────────────────────────────────────────────────────


def render_questionnaire_ui(tags: list) -> None:
    """Renders the full questionnaire. Appends selected tags to `tags` in place."""
    # Ensure persistent state keys exist
    if "saved_questionnaire_tags" not in st.session_state:
        st.session_state["saved_questionnaire_tags"] = []

    # Restore checkbox keys from backup BEFORE computing progress
    _restore_checkbox_states_from_backup()

    total = len(QUESTIONNAIRE_CONFIG)
    answered = _count_answered_questions()
    _render_progress(answered, total)

    for q_id, q_data in QUESTIONNAIRE_CONFIG.items():
        _render_question(q_id, q_data, tags)


# ─── State Synchronization & Recovery ────────────────────────────────────────


def _restore_checkbox_states_from_backup() -> None:
    """Restores deleted Streamlit keys using the persistent backup string array."""
    saved_tags = st.session_state.get("saved_questionnaire_tags", [])
    if not saved_tags:
        return

    for q_id, q_data in QUESTIONNAIRE_CONFIG.items():
        categories = q_data.get("categories", {})
        specifics = q_data.get("specifics", {})

        # Restore normal checkboxes
        for cat_opts in categories.values():
            for opt_name, tag_list in cat_opts.items():
                key = f"chk_{q_id}_{opt_name}"
                # If any of the tags in the tag_list were saved, the checkbox is True
                if any(t in saved_tags for t in tag_list):
                    st.session_state[key] = True
                elif key not in st.session_state:
                    st.session_state[key] = False

        # Restore popover checkboxes
        for section_name, options in specifics.items():
            for opt, tag_list in options.items():
                key = f"chk_opt_{q_id}_{section_name}_{opt}"
                if any(t in saved_tags for t in tag_list):
                    st.session_state[key] = True
                elif key not in st.session_state:
                    st.session_state[key] = False


def _update_saved_tags() -> None:
    """Scans current checkbox states and commits them to the persistent backup."""
    selected_tags = []
    
    for q_id, q_data in QUESTIONNAIRE_CONFIG.items():
        categories = q_data.get("categories", {})
        specifics = q_data.get("specifics", {})

        for cat_opts in categories.values():
            for opt_name, tag_list in cat_opts.items():
                key = f"chk_{q_id}_{opt_name}"
                if st.session_state.get(key, False):
                    selected_tags.extend(tag_list)

        for section_name, options in specifics.items():
            for opt, tag_list in options.items():
                key = f"chk_opt_{q_id}_{section_name}_{opt}"
                if st.session_state.get(key, False):
                    selected_tags.extend(tag_list)

    # De-duplicate while maintaining list order
    seen = set()
    st.session_state["saved_questionnaire_tags"] = [
        t for t in selected_tags if not (t in seen or seen.add(t))
    ]


# ─── Progress ────────────────────────────────────────────────────────────────


def _count_answered_questions() -> int:
    """Counts a question as answered if at least one checkbox is True."""
    answered = 0
    for q_id, q_data in QUESTIONNAIRE_CONFIG.items():
        categories = q_data.get("categories", {})
        specifics = q_data.get("specifics", {})
        question_is_answered = False

        # Check normal categories
        for cat_opts in categories.values():
            for opt_name in cat_opts:
                if st.session_state.get(f"chk_{q_id}_{opt_name}", False):
                    question_is_answered = True
                    break
            if question_is_answered:
                break

        # Check specifics popover if categories didn't match
        if not question_is_answered and specifics:
            for section_name, options in specifics.items():
                for opt in options:
                    if st.session_state.get(f"chk_opt_{q_id}_{section_name}_{opt}", False):
                        question_is_answered = True
                        break
                if question_is_answered:
                    break

        if question_is_answered:
            answered += 1

    return answered


def _render_progress(answered: int, total: int) -> None:
    dots_html = "".join(
        f'<div class="progress-dot {"done" if i < answered else ""}"></div>'
        for i in range(total)
    )
    st.markdown(
        f"""
        <div style="margin-bottom: 4px; font-size: 0.8rem; color: #8b949e;">
            Đã trả lời {answered}/{total} câu hỏi
        </div>
        <div class="progress-container">{dots_html}</div>
        """,
        unsafe_allow_html=True,
    )


# ─── Question Renderer ───────────────────────────────────────────────────────


def _render_question(q_id: str, q_data: dict, tags: list) -> None:
    is_multi = q_data.get("multi", False)
    max_select = q_data.get("max_select") if is_multi else None
    categories = q_data.get("categories", {})
    specifics = q_data.get("specifics", {})

    st.markdown(f"### {q_data['question']}")

    # All checkbox keys for this question (used for selection counting)
    all_keys = [
        f"chk_{q_id}_{opt}"
        for cat_opts in categories.values()
        for opt in cat_opts
    ]

    if categories:
        if is_multi and max_select:
            count = sum(st.session_state.get(k, False) for k in all_keys)
            remaining = max_select - count
            msg = f"Còn {remaining} lựa chọn" if remaining > 0 else f"✅ Đã chọn đủ {max_select} lựa chọn"
            st.caption(msg)

        if len(categories) == 1:
            _, cat_options = list(categories.items())[0]
            _render_option_row(q_id, cat_options, all_keys, is_multi, max_select, tags)
        else:
            cols = st.columns(len(categories))
            for col, (cat_name, cat_options) in zip(cols, categories.items()):
                with col:
                    _render_category_header(cat_name)
                    _render_option_column(q_id, cat_options, all_keys, is_multi, max_select, tags)

    if specifics:
        st.markdown("**Bạn có thể chọn thêm tùy chọn chi tiết:**")
        for section_name, options in specifics.items():
            _render_specifics_popover(q_id, section_name, options, tags)

    _render_divider()


# ─── Option Renderers ─────────────────────────────────────────────────────────


def _render_option_row(q_id, cat_options, all_keys, is_multi, max_select, tags):
    """Single-category: render all options in a horizontal row."""
    cols = st.columns(len(cat_options))
    for col, (opt_name, tag_list) in zip(cols, cat_options.items()):
        key = f"chk_{q_id}_{opt_name}"
        st.session_state.setdefault(key, False)
        with col:
            _render_checkbox(key, opt_name, all_keys, q_id, is_multi, max_select)
        if st.session_state[key]:
            tags.extend(tag_list)


def _render_option_column(q_id, cat_options, all_keys, is_multi, max_select, tags):
    """Multi-category: render options stacked vertically in a column."""
    for opt_name, tag_list in cat_options.items():
        key = f"chk_{q_id}_{opt_name}"
        st.session_state.setdefault(key, False)
        _render_checkbox(key, opt_name, all_keys, q_id, is_multi, max_select)
        if st.session_state[key]:
            tags.extend(tag_list)


def _render_checkbox(key, opt_name, all_keys, q_id, is_multi, max_select):
    emoji = EMOJI_MAP.get(opt_name, "✨")
    label = f"{emoji} {opt_name}"
    is_checked = st.session_state[key]

    if is_multi:
        count = sum(st.session_state.get(k, False) for k in all_keys)
        disabled = bool(max_select and count >= max_select and not is_checked)
        st.checkbox(
            label, 
            key=key, 
            disabled=disabled,
            on_change=_multi_select_callback
        )
    else:
        st.checkbox(
            label,
            key=key,
            on_change=_exclusive_select,
            kwargs={"selected_key": key, "all_keys": all_keys},
        )


def _exclusive_select(selected_key: str, all_keys: list) -> None:
    """Callback for single-choice checkboxes."""
    if st.session_state[selected_key]:
        for k in all_keys:
            if k != selected_key:
                st.session_state[k] = False
    _update_saved_tags()


def _multi_select_callback() -> None:
    """Callback for multi-choice checkboxes."""
    _update_saved_tags()


# ─── Specifics Popover ────────────────────────────────────────────────────────


def _render_specifics_popover(q_id, section_name, options, tags):
    spec_keys = [f"chk_opt_{q_id}_{section_name}_{opt}" for opt in options]
    max_spec = 3

    with st.popover(section_name, use_container_width=True):
        with st.container(height=250):
            spec_count = sum(st.session_state.get(k, False) for k in spec_keys)
            remaining = max_spec - spec_count
            msg = f"Còn {remaining} lựa chọn" if remaining > 0 else f"✅ Đã chọn đủ {max_spec}"
            st.caption(msg)

            for opt, tag_list in options.items():
                key = f"chk_opt_{q_id}_{section_name}_{opt}"
                st.session_state.setdefault(key, False)
                is_checked = st.session_state[key]
                disabled = spec_count >= max_spec and not is_checked
                emoji = EMOJI_MAP.get(opt, "✨")
                
                st.checkbox(
                    f"{emoji} {opt}", 
                    key=key, 
                    disabled=disabled,
                    on_change=_update_saved_tags
                )
                if st.session_state[key]:
                    tags.extend(tag_list)


# ─── Helpers ──────────────────────────────────────────────────────────────────


def _render_category_header(cat_name: str) -> None:
    st.markdown(
        f"""
        <div style="
            text-align: center;
            font-weight: 700;
            font-size: 1rem;
            color: #e6edf3;
            margin-bottom: 10px;
            padding-bottom: 5px;
            border-bottom: 2px solid #ff6b6b;
        ">{cat_name}</div>
        """,
        unsafe_allow_html=True,
    )


def _render_divider() -> None:
    st.markdown(
        "<div style='margin-bottom: 50px; border-bottom: 1px solid #30363d;'></div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)
