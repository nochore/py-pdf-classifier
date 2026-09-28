"""Unit tests for utility functions and session state initializers."""

from unittest.mock import patch

import streamlit as st

from pdf_classifier.utils.state import init_session_state
from pdf_classifier.utils.styles import apply_custom_styles


def test_init_session_state():
    """Test session state variables are initialized properly."""
    # Simulate st.session_state as dict
    session_dict = {}
    with patch.object(st, "session_state", session_dict):
        init_session_state()
        assert "pdf_bytes" in session_dict
        assert session_dict["pdf_bytes"] is None
        assert "extracted_text" in session_dict
        assert session_dict["extracted_text"] == ""
        assert "doc_metrics" in session_dict
        assert session_dict["doc_metrics"] == {}
        assert "ai_summary" in session_dict
        assert "chat_history" in session_dict
        assert session_dict["chat_history"] == []


@patch("pdf_classifier.utils.styles.st.markdown")
def test_apply_custom_styles(mock_markdown):
    """Test apply_custom_styles injects custom CSS."""
    apply_custom_styles()
    mock_markdown.assert_called_once()
    args, kwargs = mock_markdown.call_args
    assert "<style>" in args[0]
    assert kwargs.get("unsafe_allow_html") is True
