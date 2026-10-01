"""Unit tests for utility functions and session state initializers."""

from unittest.mock import MagicMock, patch

import streamlit as st

from pdf_classifier.utils.state import init_session_state, reset_session_state
from pdf_classifier.utils.styles import (
    apply_custom_styles,
    empty_state,
    html,
    kpi,
    kpi_row,
    panel_title,
)


class MockSessionState(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


def test_init_session_state():
    """Test session state variables are initialized properly."""
    session_dict = MockSessionState()
    with patch.object(st, "session_state", session_dict):
        init_session_state()
        assert "pdf_bytes" in session_dict
        assert session_dict.pdf_bytes is None
        assert "extracted_text" in session_dict
        assert session_dict.extracted_text == ""
        assert "doc_metrics" in session_dict
        assert session_dict.doc_metrics == {}
        assert "ai_summary" in session_dict
        assert "chat_history" in session_dict
        assert session_dict.chat_history == []


def test_reset_session_state():
    """Test reset_session_state clears document state variables."""
    session_dict = MockSessionState(
        {
            "extracted_text": "text",
            "ai_summary": "summary",
            "doc_metrics": {"page_count": 5},
            "chat_history": [{"role": "user", "content": "hi"}],
            "pdf_bytes": b"bytes",
            "uploaded_file_name": "file.pdf",
            "extraction_result": "result",
            "latency_ms": 120,
        }
    )
    with patch.object(st, "session_state", session_dict):
        reset_session_state()
        assert session_dict.extracted_text == ""
        assert session_dict.ai_summary == ""
        assert session_dict.doc_metrics == {}
        assert session_dict.chat_history == []
        assert session_dict.pdf_bytes is None
        assert session_dict.uploaded_file_name == ""
        assert session_dict.extraction_result is None
        assert session_dict.latency_ms is None


@patch("pdf_classifier.utils.styles.st.markdown")
def test_apply_custom_styles(mock_markdown):
    """Test apply_custom_styles injects custom CSS."""
    apply_custom_styles()
    mock_markdown.assert_called_once()
    args, kwargs = mock_markdown.call_args
    assert "<style>" in args[0]
    assert kwargs.get("unsafe_allow_html") is True


@patch("pdf_classifier.utils.styles.st.markdown")
def test_styles_helpers(mock_markdown):
    """Test HTML and styling helper functions."""
    html("<div>test</div>")
    mock_markdown.assert_called_with("<div>test</div>", unsafe_allow_html=True)

    panel_title("My Panel", "Meta info")
    kpi_html = kpi("Pages", "10", "total", ok=True)
    assert '<div class="kpi">' in kpi_html
    assert "s ok" in kpi_html

    kpi_html_false = kpi("Pages", "10", "total", ok=False)
    assert 'class="s"' in kpi_html_false

    empty_state("No data found")


@patch("pdf_classifier.utils.styles.st.columns")
def test_kpi_row(mock_columns):
    """Test kpi_row helper."""
    col1 = MagicMock()
    col2 = MagicMock()
    mock_columns.return_value = [col1, col2]
    items = [("Label 1", "Val 1", "Sub 1", True), ("Label 2", "Val 2", "Sub 2", False)]
    kpi_row(items)
    mock_columns.assert_called_once_with(2, gap="small")
