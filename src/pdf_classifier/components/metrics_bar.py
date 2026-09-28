"""Metrics bar component for document quantitative metrics display."""

import streamlit as st


def render_metrics_bar() -> None:
    """Render 5-column metric display banner for document quantitative statistics."""
    metrics = st.session_state.doc_metrics
    if not metrics:
        return

    m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)

    with m_col1:
        st.metric("Total Pages", metrics.get("page_count", 0))

    with m_col2:
        st.metric("Word Count", f"{metrics.get('word_count', 0):,}")

    with m_col3:
        st.metric("Character Count", f"{metrics.get('char_count', 0):,}")

    with m_col4:
        st.metric("Avg Word Length", f"{metrics.get('avg_word_length', 0)} chars")

    with m_col5:
        st.metric("Est. Read Time", f"{metrics.get('reading_time_min', 0)} min")

    st.divider()
