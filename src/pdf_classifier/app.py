"""Main Streamlit application entry point for Document AI Enterprise Parser."""

import streamlit as st

from pdf_classifier.components import (
    render_chat_workspace,
    render_raw_schema,
    render_sidebar,
    render_split_inspector,
)
from pdf_classifier.utils import apply_custom_styles, init_session_state


def render_header() -> None:
    """Render the top navigation bar with branding and segmented view switcher."""
    active_doc = st.session_state.uploaded_file_name or "01_valid_invoice.pdf"

    h_col1, h_col2, h_col3 = st.columns([3, 4, 3])

    with h_col1:
        st.markdown(
            f'<div style="display: flex; align-items: center; gap: 10px; padding-top: 4px;">'
            f'<div style="font-size: 15px; font-weight: 700; color: #f1f5f9; display: flex; align-items: center; gap: 6px;">'
            f'<span style="background: rgba(59, 130, 246, 0.2); color: #3b82f6; padding: 2px 6px; border-radius: 4px;">📄</span> Document AI'
            f'</div>'
            f'<div style="height: 14px; width: 1px; background: #222f3d;"></div>'
            f'<div style="font-family: monospace; font-size: 11px; color: #94a3b8; background: #141c24; padding: 2px 8px; border-radius: 4px; border: 1px solid #222f3d; display: flex; align-items: center; gap: 6px;">'
            f'<span>{active_doc}</span><span style="color: #10b981;">●</span>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with h_col2:
        views = ["Split Inspector", "Q&A Chat", "Raw Schema"]
        st.radio(
            "",
            options=views,
            key="active_view",
            horizontal=True,
            label_visibility="collapsed",
        )

    with h_col3:
        st.markdown(
            '<div style="display: flex; align-items: center; justify-content: flex-end; gap: 8px; padding-top: 4px;">'
            '<div style="font-family: monospace; font-size: 11px; color: #94a3b8; background: #141c24; padding: 3px 8px; border-radius: 4px; border: 1px solid #222f3d; display: flex; align-items: center; gap: 6px;">'
            '<span style="color: #10b981;">●</span><span>Ollama: llama3</span>'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )


def render_status_bar(model_name: str) -> None:
    """Render bottom ambient telemetry status bar dock."""
    st.markdown(
        f'<div class="footer-dock">'
        f'<div>Model: <span style="color: #f1f5f9;">{model_name}</span> • Speed: <span style="color: #f1f5f9;">48.2 tok/s</span> • Context: <span style="color: #f1f5f9;">3.1k / 8k</span></div>'
        f'<div><span class="online-dot">● Local Offline Engine</span></div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def main() -> None:
    """Initialize and run the Streamlit Document AI application."""
    st.set_page_config(
        page_title="Document AI Enterprise Parser",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    apply_custom_styles()
    init_session_state()

    model_name = render_sidebar()

    render_header()

    if st.session_state.extracted_text:
        current_view = st.session_state.active_view
        if current_view == "Split Inspector":
            render_split_inspector()
        elif current_view == "Q&A Chat":
            render_chat_workspace(model_name)
        elif current_view == "Raw Schema":
            render_raw_schema()
        else:
            render_split_inspector()
    else:
        st.info(
            "System Ready. Please upload a PDF document in the "
            "sidebar configuration panel to initialize analysis."
        )

    render_status_bar(model_name)


if __name__ == "__main__":
    main()
