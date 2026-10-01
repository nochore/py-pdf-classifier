"""Sidebar component for configuration and document uploading."""

import time
from html import escape

import streamlit as st

from pdf_classifier.services.metrics_service import compute_text_metrics
from pdf_classifier.services.ollama_service import query_ollama
from pdf_classifier.services.pdf_service import extract_pdf_data
from pdf_classifier.utils.styles import html

PRESETS = {
    "Invoice": "Focus on invoice fields: vendor, invoice number, dates, line items and totals.",
    "Academic": "Focus on academic structure: title, authors, abstract, methods and findings.",
    "Summary": "Focus on a general-purpose summary of the document.",
}


def _run_extraction(uploaded_file, model_name: str, temperature: float) -> None:
    """Extract PDF text, compute metrics and request the AI summary."""
    raw_bytes = uploaded_file.getvalue()
    extracted_text, page_count = extract_pdf_data(raw_bytes)

    st.session_state.pdf_bytes = raw_bytes
    st.session_state.extracted_text = extracted_text
    st.session_state.uploaded_file_name = uploaded_file.name
    st.session_state.doc_metrics = compute_text_metrics(extracted_text, page_count)

    preset = st.session_state.schema_preset or "Summary"
    analysis_query = (
        "Analyze the following text extracted from a document. "
        f"{PRESETS[preset]} Provide a response with these exact sections:\n"
        "1. Document Classification Type\n"
        "2. Key Metadata (Dates, Entities, Organizations)\n"
        "3. Executive Summary (3 structured sentences)\n\n"
        f"Document Text:\n{extracted_text[:6000]}"
    )
    started = time.perf_counter()
    st.session_state.ai_summary = query_ollama(
        prompt=analysis_query,
        model=model_name,
        system_prompt=(
            "You are an automated document analysis service. "
            "Provide structured, high-density analysis using precise markdown."
        ),
        temperature=temperature,
    )
    st.session_state.latency_ms = int((time.perf_counter() - started) * 1000)
    st.session_state.chat_history = []

    recent = [f for f in st.session_state.recent_files if f != uploaded_file.name]
    st.session_state.recent_files = [uploaded_file.name, *recent][:5]


def render_sidebar() -> str:
    """Render the persistent left sidebar and return the target model name."""
    with st.sidebar:
        html(
            '<div class="brand" style="height:auto">'
            '<span class="brand-mark">⚡</span>Document AI</div>'
            '<div style="font-size:11px;color:var(--text-3);margin:2px 0 14px">'
            "Local AI extraction workbench</div>"
        )

        html('<div class="eyebrow">Target document</div>')
        uploaded_file = st.file_uploader(
            "Select Target Document (PDF)", type=["pdf"], key="pdf_uploader"
        )
        if uploaded_file is not None:
            st.session_state.uploaded_file_name = uploaded_file.name
            size_kb = max(1, uploaded_file.size // 1024)
            pages = st.session_state.doc_metrics.get("page_count")
            meta = f"{size_kb} KB" + (f" • {pages} pg" if pages else "")
            html(
                f'<div class="row"><div>{escape(uploaded_file.name)}'
                f"<small class='mono'>{meta}</small></div>"
                '<span style="color:var(--ok)">✓</span></div>'
            )

        if st.session_state.recent_files:
            html('<div class="eyebrow" style="margin-top:1rem">Recent files</div>')
            html(
                "".join(
                    f'<div class="row" style="padding:5px 10px;font-size:12px;'
                    f'color:var(--text-2)">{escape(name)}</div>'
                    for name in st.session_state.recent_files
                )
            )

        html('<div class="eyebrow" style="margin-top:1rem">Inference · Ollama</div>')
        model_name = st.text_input(
            "Ollama Model Identifier",
            value="llama3",
            key="input_model_name",
            help="Target model instance running on localhost",
        )
        temperature = st.slider(
            "Temperature",
            0.0,
            1.0,
            0.10,
            0.05,
            key="input_temperature",
            help="Lower values give more deterministic output",
        )
        st.number_input(
            "Max detected values",
            min_value=1,
            max_value=1000,
            value=200,
            step=10,
            key="max_entities",
            help="Maximum amounts and dates detected (and boxed on the PDF) per type",
        )
        st.segmented_control(
            "Extraction schema",
            list(PRESETS),
            default="Summary",
            key="schema_preset",
        )

        parse_btn = st.button(
            "Execute extraction",
            icon=":material/bolt:",
            type="primary",
            key="btn_parse_doc",
            width="stretch",
            disabled=uploaded_file is None,
        )
        if parse_btn and uploaded_file is not None:
            with st.spinner("Processing document..."):
                _run_extraction(uploaded_file, model_name, temperature)

    return model_name
