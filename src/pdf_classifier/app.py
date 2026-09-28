"""Main Streamlit application entry point for Document AI Enterprise Parser."""

import streamlit as st

from pdf_classifier.components import (
    render_export_view,
    render_metrics_bar,
    render_pdf_viewer,
    render_qa_chat,
    render_search_view,
    render_sidebar,
    render_summary_view,
)
from pdf_classifier.utils import apply_custom_styles, init_session_state


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

    st.title("Document Analysis Dashboard")

    if st.session_state.extracted_text:
        render_metrics_bar()

        tab_preview, tab_summary, tab_search, tab_qa, tab_raw = st.tabs([
            "PDF Viewer",
            "Executive Summary",
            "Text Inspection & Search",
            "Document Q&A Workspace",
            "Raw Data & Export",
        ])

        with tab_preview:
            render_pdf_viewer()

        with tab_summary:
            render_summary_view()

        with tab_search:
            render_search_view()

        with tab_qa:
            render_qa_chat(model_name)

        with tab_raw:
            render_export_view()
    else:
        st.info(
            "System Ready. Please upload a PDF document in the "
            "sidebar configuration panel to initialize analysis."
        )


if __name__ == "__main__":
    main()
