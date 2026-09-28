"""Keyword search inspection tab component."""

import streamlit as st

from pdf_classifier.services.metrics_service import highlight_keywords


def render_search_view() -> None:
    """Render keyword search interface with highlighted text payload."""
    st.subheader("Document Keyword Search")
    search_query = st.text_input(
        "Enter term to locate in payload:",
        key="input_search_query",
        placeholder="e.g. Total, Agreement, Date, Confidential",
    )

    if search_query:
        with st.spinner("Scanning document payload..."):
            highlighted_html, count = highlight_keywords(
                st.session_state.extracted_text, search_query
            )

        st.markdown(
            '<div data-testid="search-count-badge" '
            'style="margin-bottom: 12px; font-weight: 500;">'
            f'Found <span style="color: #3b82f6; font-weight: 700;">{count}</span> '
            f'occurrences of "{search_query}"</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div data-testid="search-results-box" style="background-color: '
            'var(--secondary-background-color); padding: 16px; border: 1px solid '
            'rgba(255,255,255,0.1); border-radius: 6px; max-height: 400px; '
            'overflow-y: auto; white-space: pre-wrap; font-family: monospace; '
            f'font-size: 13px; color: var(--text-color);">{highlighted_html}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.info(
            "Enter a term above to dynamically locate occurrences across "
            "the extracted text payload."
        )
