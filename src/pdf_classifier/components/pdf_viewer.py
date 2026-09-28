"""PDF visual inspector tab component."""

import streamlit as st

from pdf_classifier.services.pdf_service import render_pdf_page_cached


def render_pdf_viewer() -> None:
    """Render interactive PDF page preview with page navigation and zoom controls."""
    st.subheader("PDF Visual Inspector")
    metrics = st.session_state.doc_metrics
    total_pages = metrics.get("page_count", 1)

    ctrl_col1, ctrl_col2 = st.columns([1, 3])
    with ctrl_col1:
        selected_page = st.number_input(
            "Page Navigation",
            min_value=1,
            max_value=max(1, total_pages),
            value=1,
            step=1,
            key="input_pdf_preview_page",
        )

    with ctrl_col2:
        zoom_level = st.select_slider(
            "Rendering Resolution",
            options=[1.0, 1.5, 2.0, 2.5],
            value=2.0,
            key="select_pdf_zoom",
        )

    with st.spinner("Rendering PDF page canvas..."):
        page_img = render_pdf_page_cached(
            st.session_state.pdf_bytes,
            page_number=selected_page - 1,
            zoom=zoom_level,
        )

    if page_img:
        st.markdown(
            '<div data-testid="pdf-preview-container" style="text-align: center; '
            'border: 1px solid rgba(255,255,255,0.1); padding: 12px; border-radius: 6px; '
            'background-color: var(--secondary-background-color);"></div>',
            unsafe_allow_html=True,
        )
        st.image(page_img, caption=f"Page {selected_page} of {total_pages}")
