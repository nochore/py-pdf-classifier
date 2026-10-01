"""Structured schema and raw data export component (View 3)."""

import json

import streamlit as st

from pdf_classifier.services.metrics_service import extract_entities
from pdf_classifier.utils.styles import empty_state, kpi_row, panel_title


def detect_entities() -> dict[str, list[str]]:
    """Detect amounts/dates using the user-configured maximum per type."""
    limit = int(st.session_state.get("max_entities", 200))
    return extract_entities(st.session_state.extracted_text, limit=limit)


def build_extraction_payload() -> dict:
    """Assemble the structured extraction payload from session state."""
    state = st.session_state
    return {
        "document": state.uploaded_file_name,
        "metrics": state.doc_metrics,
        "entities": detect_entities(),
        "summary": state.ai_summary,
    }


def render_export_view() -> None:
    """Render the schema view: KPIs, detected values table, code editor and downloads."""
    payload = build_extraction_payload()
    metrics = st.session_state.doc_metrics
    entities = payload["entities"]
    json_text = json.dumps(payload, indent=2)
    col_left, col_right = st.columns([7, 5], gap="medium")

    with col_left:
        kpi_row(
            [
                ("Characters", f"{metrics.get('char_count', 0):,}", "extracted text", False),
                ("Avg word length", str(metrics.get("avg_word_length", 0)), "characters", False),
                ("Schema", "Valid JSON", "RFC 8259", True),
            ]
        )
        with st.container(border=True):
            rows = [("Amount", v) for v in entities["amounts"]] + [
                ("Date", v) for v in entities["dates"]
            ]
            panel_title("Detected values", f"{len(rows)} records")
            if rows:
                st.dataframe(
                    [{"Type": t, "Value": v} for t, v in rows],
                    hide_index=True,
                    width="stretch",
                )
            else:
                empty_state("No amounts or dates detected in the extracted text.")

        with st.container(horizontal=True):
            st.download_button(
                "Download raw text",
                data=st.session_state.extracted_text,
                file_name="extracted_document.txt",
                mime="text/plain",
                icon=":material/download:",
                key="btn_download_txt",
            )
            st.download_button(
                "Download JSON report",
                data=json.dumps({**payload, "raw_text": st.session_state.extracted_text}, indent=2),
                file_name="audit_report.json",
                mime="application/json",
                icon=":material/data_object:",
                key="btn_download_json",
            )

    with col_right, st.container(border=True):
        panel_title("Schema editor", "UTF-8 • valid JSON")
        tab_json, tab_raw = st.tabs(["JSON", "Raw text"])
        with tab_json:
            st.code(json_text, language="json", line_numbers=True)
        with tab_raw:
            st.text_area(
                "Raw Text Data",
                value=st.session_state.extracted_text,
                height=360,
                key="raw_text_inspector",
                label_visibility="collapsed",
            )


def render_raw_schema() -> None:
    """Alias for render_export_view."""
    render_export_view()
