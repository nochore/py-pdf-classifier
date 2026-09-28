"""Session state management for PDF Classifier."""

from typing import Any

import streamlit as st


def init_session_state() -> None:
    """Initialize default keys and values in Streamlit session state."""
    defaults: dict[str, Any] = {
        "extracted_text": "",
        "ai_summary": "",
        "doc_metrics": {},
        "chat_history": [],
        "pdf_bytes": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_session_state() -> None:
    """Clear and reset all document-specific session state."""
    st.session_state.extracted_text = ""
    st.session_state.ai_summary = ""
    st.session_state.doc_metrics = {}
    st.session_state.chat_history = []
    st.session_state.pdf_bytes = None
