"""Raw data inspection and export controls tab component."""

import json

import streamlit as st


def render_export_view() -> None:
    """Render raw text inspector and report download buttons."""
    st.subheader("Extracted Text Payload")
    st.text_area(
        label="Raw Text Data",
        value=st.session_state.extracted_text,
        height=300,
        key="raw_text_inspector",
    )

    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        st.download_button(
            label="Download Raw Text File",
            data=st.session_state.extracted_text,
            file_name="extracted_document.txt",
            mime="text/plain",
            key="btn_download_txt",
        )
    with col_exp2:
        export_payload = {
            "metrics": st.session_state.doc_metrics,
            "summary": st.session_state.ai_summary,
            "raw_text": st.session_state.extracted_text,
        }
        st.download_button(
            label="Download Full JSON Audit Report",
            data=json.dumps(export_payload, indent=2),
            file_name="audit_report.json",
            mime="application/json",
            key="btn_download_json",
        )
