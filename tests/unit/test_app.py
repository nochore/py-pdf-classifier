"""Unit tests for app.py main application entry point and header/status components."""

from unittest.mock import MagicMock, patch

import pymupdf
import pytest
import streamlit as st

from pdf_classifier.app import main, render_header, render_status_bar


class MockSessionState(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError(f"'MockSessionState' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError(f"'MockSessionState' object has no attribute '{name}'")


@pytest.fixture
def sample_pdf_bytes() -> bytes:
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Sample PDF text")
    raw_bytes = doc.tobytes()
    doc.close()
    return raw_bytes


def create_app_state(pdf_bytes: bytes, extracted: bool = True):
    return MockSessionState(
        {
            "uploaded_file_name": "invoice_101.pdf" if extracted else "",
            "active_view": "Split Inspector",
            "extracted_text": "Sample PDF text" if extracted else "",
            "doc_metrics": (
                {
                    "page_count": 1,
                    "word_count": 10,
                    "char_count": 50,
                    "avg_word_length": 5.0,
                    "reading_time_min": 0.1,
                }
                if extracted
                else {}
            ),
            "latency_ms": 250 if extracted else None,
            "pdf_bytes": pdf_bytes if extracted else None,
            "recent_files": ["invoice_101.pdf"] if extracted else [],
            "ai_summary": "Summary" if extracted else "",
            "chat_history": [],
            "max_entities": 200,
            "schema_preset": "Summary",
            "input_temperature": 0.1,
        }
    )


@patch("pdf_classifier.app.st")
def test_render_header(mock_st, sample_pdf_bytes):
    """Test render_header with document set and with empty document."""
    state = create_app_state(sample_pdf_bytes, extracted=True)
    mock_st.session_state = state
    c1, c2, c3 = MagicMock(), MagicMock(), MagicMock()
    mock_st.columns.return_value = [c1, c2, c3]
    mock_st.segmented_control.return_value = "Q&A Chat"

    with patch.object(st, "session_state", state):
        render_header("llama3")
        assert state.active_view == "Q&A Chat"

    # Test header when no document loaded
    empty_state = create_app_state(sample_pdf_bytes, extracted=False)
    mock_st.session_state = empty_state
    mock_st.segmented_control.return_value = None
    with patch.object(st, "session_state", empty_state):
        render_header("llama3")


@patch("pdf_classifier.app.html")
def test_render_status_bar(mock_html, sample_pdf_bytes):
    """Test render_status_bar with metrics and latency."""
    state = create_app_state(sample_pdf_bytes, extracted=True)
    with patch.object(st, "session_state", state):
        render_status_bar("llama3")
        mock_html.assert_called_once()


@patch("pdf_classifier.app.render_status_bar")
@patch("pdf_classifier.app.render_split_inspector")
@patch("pdf_classifier.app.render_raw_schema")
@patch("pdf_classifier.app.render_chat_workspace")
@patch("pdf_classifier.app.render_header")
@patch("pdf_classifier.app.render_sidebar")
@patch("pdf_classifier.app.st")
def test_main_views(
    mock_st,
    mock_sidebar,
    mock_header,
    mock_chat,
    mock_schema,
    mock_split,
    mock_status,
    sample_pdf_bytes,
):
    """Test main function rendering each active view and empty state."""
    mock_sidebar.return_value = "llama3"

    # 1. Test Split Inspector View
    state_split = create_app_state(sample_pdf_bytes, extracted=True)
    state_split.active_view = "Split Inspector"
    mock_st.session_state = state_split
    with patch.object(st, "session_state", state_split):
        main()
        mock_split.assert_called_once()

    # 2. Test Q&A Chat View
    state_chat = create_app_state(sample_pdf_bytes, extracted=True)
    state_chat.active_view = "Q&A Chat"
    mock_st.session_state = state_chat
    with patch.object(st, "session_state", state_chat):
        main()
        mock_chat.assert_called_once_with("llama3")

    # 3. Test Raw Schema View
    state_schema = create_app_state(sample_pdf_bytes, extracted=True)
    state_schema.active_view = "Raw Schema"
    mock_st.session_state = state_schema
    with patch.object(st, "session_state", state_schema):
        main()
        mock_schema.assert_called_once()

    # 4. Test Empty State (No extracted text)
    state_empty = create_app_state(sample_pdf_bytes, extracted=False)
    mock_st.session_state = state_empty
    with patch.object(st, "session_state", state_empty):
        main()
