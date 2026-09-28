"""Sidebar component for configuration and document uploading."""

import streamlit as st

from pdf_classifier.services.metrics_service import compute_text_metrics
from pdf_classifier.services.ollama_service import query_ollama
from pdf_classifier.services.pdf_service import extract_pdf_data


def render_sidebar() -> str:
    """Render the sidebar UI for system parameters and file upload.

    Returns:
        The target model name string.
    """
    model_name = "llama3"

    with st.sidebar:
        st.title("Document AI Engine")
        st.caption("Enterprise PDF Analytics & Intelligence Platform")
        st.divider()

        st.subheader("System Configuration")
        model_name = st.text_input(
            "Ollama Model Identifier",
            value="llama3",
            key="input_model_name",
            help="Target model instance running on localhost",
        )

        uploaded_file = st.file_uploader(
            "Select Target Document (PDF)",
            type=["pdf"],
            key="pdf_uploader",
        )

        parse_btn = st.button(
            "Execute Document Extraction",
            type="primary",
            key="btn_parse_doc",
        )

        if parse_btn and uploaded_file is not None:
            with st.spinner("Processing document payload..."):
                raw_bytes = uploaded_file.read()
                extracted_text, page_count = extract_pdf_data(raw_bytes)

                st.session_state.pdf_bytes = raw_bytes
                st.session_state.extracted_text = extracted_text
                st.session_state.doc_metrics = compute_text_metrics(extracted_text, page_count)

                sys_prompt = (
                    "You are an automated document analysis service. "
                    "Provide structured, high-density analysis using precise markdown."
                )
                analysis_query = (
                    "Analyze the following text extracted from a document. "
                    "Provide a response with these exact sections:\n"
                    "1. Document Classification Type\n"
                    "2. Key Metadata (Dates, Entities, Organizations)\n"
                    "3. Executive Summary (3 structured sentences)\n\n"
                    f"Document Text:\n{extracted_text[:6000]}"
                )

                st.session_state.ai_summary = query_ollama(
                    prompt=analysis_query,
                    model=model_name,
                    system_prompt=sys_prompt,
                )
                st.session_state.chat_history = []

    return model_name
