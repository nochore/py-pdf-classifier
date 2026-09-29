"""Sidebar component for configuration and document uploading."""

import streamlit as st

from pdf_classifier.services.metrics_service import compute_text_metrics
from pdf_classifier.services.ollama_service import query_ollama
from pdf_classifier.services.pdf_service import extract_pdf_data


def render_sidebar() -> str:
    """Render the persistent left sidebar for utility and inference config.

    Returns:
        The target model name string.
    """
    model_name = "llama3"

    with st.sidebar:
        st.markdown(
            '<div style="font-size: 14px; font-weight: 600; color: #f1f5f9; margin-bottom: 2px;">'
            '<span style="color: #3b82f6;">⚡</span> Document AI</div>'
            '<div style="font-size: 11px; color: #64748b; margin-bottom: 12px;">'
            'Local AI Extraction Workbench</div>',
            unsafe_allow_html=True,
        )

        # Target Document Card or Upload Action
        st.markdown(
            '<div style="font-size: 10px; font-weight: 500; text-transform: uppercase; '
            'color: #8c909f; letter-spacing: 0.04em; margin-bottom: 4px;">Target Document</div>',
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader(
            "Select Target Document (PDF)",
            type=["pdf"],
            key="pdf_uploader",
        )

        if uploaded_file is not None:
            st.session_state.uploaded_file_name = uploaded_file.name
            size_kb = len(uploaded_file.getvalue()) // 1024
            pg_count = st.session_state.doc_metrics.get("page_count", 1)
            st.markdown(
                f'<div class="slate-card-sm" style="display: flex; align-items: center; justify-content: space-between;">'
                f'<div>'
                f'<div style="font-size: 12px; font-weight: 500; color: #f0f6fc; overflow: hidden; text-overflow: ellipsis; max-width: 170px; white-space: nowrap;">{uploaded_file.name}</div>'
                f'<div style="font-size: 10px; color: #8b949e; font-family: monospace;">{size_kb} KB • {pg_count} pg</div>'
                f'</div>'
                f'<span style="color: #10b981; font-size: 16px;">✓</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)

        # Recent Files Artifacts List
        st.markdown(
            '<div style="font-size: 10px; font-weight: 500; text-transform: uppercase; '
            'color: #8c909f; letter-spacing: 0.04em; margin-bottom: 6px;">Recent Artifacts</div>',
            unsafe_allow_html=True,
        )
        recent_html = """
        <div style="display: flex; flex-direction: column; gap: 4px;">
            <div style="display: flex; justify-content: space-between; font-size: 11px; padding: 4px 8px; background: #141c24; border-radius: 4px; color: #94a3b8;">
                <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">q4_balance_sheet.pdf</span>
                <span style="color: #64748b; font-size: 10px;">2h ago</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 11px; padding: 4px 8px; background: #141c24; border-radius: 4px; color: #94a3b8;">
                <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">nda_revised_draft.pdf</span>
                <span style="color: #64748b; font-size: 10px;">1d ago</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 11px; padding: 4px 8px; background: #141c24; border-radius: 4px; color: #94a3b8;">
                <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">w9_contractor_fill.pdf</span>
                <span style="color: #64748b; font-size: 10px;">3d ago</span>
            </div>
        </div>
        """
        st.markdown(recent_html, unsafe_allow_html=True)

        st.markdown('<div style="height: 12px; border-bottom: 1px solid #222f3d;"></div>', unsafe_allow_html=True)
        st.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)

        # Runtime Inference Settings
        st.markdown(
            '<div style="font-size: 10px; font-weight: 500; text-transform: uppercase; '
            'color: #8c909f; letter-spacing: 0.04em; margin-bottom: 6px; display: flex; justify-content: space-between;">'
            '<span>Runtime Inference</span><span style="color: #10b981; font-family: monospace;">Ollama</span></div>',
            unsafe_allow_html=True,
        )

        model_name = st.text_input(
            "Ollama Model Identifier",
            value="llama3",
            key="input_model_name",
            help="Target model instance running on localhost",
        )

        st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.10,
            step=0.05,
            key="input_temperature",
            help="0.10 (Deterministic)",
        )

        st.markdown(
            '<div style="font-size: 10px; font-weight: 500; text-transform: uppercase; '
            'color: #8c909f; letter-spacing: 0.04em; margin-top: 6px; margin-bottom: 4px;">Extraction Schema</div>',
            unsafe_allow_html=True,
        )
        schema_col1, schema_col2, schema_col3 = st.columns(3)
        with schema_col1:
            st.button("Invoice", key="btn_schema_invoice", use_container_width=True)
        with schema_col2:
            st.button("Academic", key="btn_schema_academic", use_container_width=True)
        with schema_col3:
            st.button("Summary", key="btn_schema_summary", use_container_width=True)

        st.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True)

        parse_btn = st.button(
            "⚡ Execute Extraction ⌘↵",
            type="primary",
            key="btn_parse_doc",
            use_container_width=True,
        )

        if parse_btn and uploaded_file is not None:
            with st.spinner("Processing document payload..."):
                raw_bytes = uploaded_file.read()
                extracted_text, page_count = extract_pdf_data(raw_bytes)

                st.session_state.pdf_bytes = raw_bytes
                st.session_state.extracted_text = extracted_text
                st.session_state.uploaded_file_name = uploaded_file.name
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
