"""Unit tests for UI components package."""

from unittest.mock import MagicMock, patch

import pymupdf
import pytest
import streamlit as st

from pdf_classifier.components.export_view import (
    build_extraction_payload,
    detect_entities,
    render_export_view,
    render_raw_schema,
)
from pdf_classifier.components.metrics_bar import render_metrics_bar
from pdf_classifier.components.pdf_viewer import (
    render_pdf_viewer,
    render_split_inspector,
)
from pdf_classifier.components.qa_chat import (
    _queue_suggestion,
    _render_message,
    render_chat_workspace,
    render_qa_chat,
)
from pdf_classifier.components.search_view import render_search_view
from pdf_classifier.components.sidebar import _run_extraction, render_sidebar
from pdf_classifier.components.summary_view import render_summary_view


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
    page.insert_text((50, 50), "Sample PDF content $100.00 2023-01-01")
    raw_bytes = doc.tobytes()
    doc.close()
    return raw_bytes


def create_mock_state(pdf_bytes: bytes):
    return MockSessionState(
        {
            "max_entities": 100,
            "extracted_text": "Sample document text with $100.00 and 2023-01-01.",
            "uploaded_file_name": "test.pdf",
            "doc_metrics": {
                "page_count": 1,
                "word_count": 100,
                "char_count": 500,
                "avg_word_length": 5.0,
                "reading_time_min": 0.5,
            },
            "ai_summary": "Executive summary text.",
            "pdf_bytes": pdf_bytes,
            "chat_history": [],
            "recent_files": [],
            "schema_preset": "Summary",
            "active_view": "Split Inspector",
            "latency_ms": 150,
            "input_temperature": 0.1,
        }
    )


def test_detect_entities_and_build_payload(sample_pdf_bytes):
    """Test detect_entities and build_extraction_payload."""
    state = create_mock_state(sample_pdf_bytes)
    with patch.object(st, "session_state", state):
        entities = detect_entities()
        assert "$100.00" in entities["amounts"]
        assert "2023-01-01" in entities["dates"]

        payload = build_extraction_payload()
        assert payload["document"] == "test.pdf"
        assert payload["summary"] == "Executive summary text."
        assert payload["metrics"] == state.doc_metrics
        assert payload["entities"] == entities


@patch("pdf_classifier.components.export_view.st")
def test_render_export_view(mock_st, sample_pdf_bytes):
    """Test render_export_view and alias render_raw_schema."""
    state = create_mock_state(sample_pdf_bytes)
    col1, col2 = MagicMock(), MagicMock()
    col1.__enter__ = MagicMock(return_value=col1)
    col1.__exit__ = MagicMock(return_value=None)
    col2.__enter__ = MagicMock(return_value=col2)
    col2.__exit__ = MagicMock(return_value=None)
    mock_st.columns.return_value = [col1, col2]
    mock_st.tabs.return_value = [MagicMock(), MagicMock()]
    mock_st.session_state = state

    with patch.object(st, "session_state", state):
        render_export_view()
        mock_st.columns.assert_called_once()
        render_raw_schema()


@patch("pdf_classifier.components.metrics_bar.st")
def test_render_metrics_bar(mock_st, sample_pdf_bytes):
    """Test render_metrics_bar with and without metrics."""
    state = create_mock_state(sample_pdf_bytes)
    cols = [MagicMock() for _ in range(5)]
    mock_st.columns.return_value = cols
    mock_st.session_state = state

    with patch.object(st, "session_state", state):
        render_metrics_bar()
        mock_st.metric.assert_called()

        state.doc_metrics = {}
        mock_st.reset_mock()
        render_metrics_bar()
        mock_st.metric.assert_not_called()


@patch("pdf_classifier.components.pdf_viewer.render_pdf_page_cached")
@patch("pdf_classifier.components.pdf_viewer.st")
def test_render_pdf_stage_and_inspector(mock_st, mock_render_pdf_page, sample_pdf_bytes):
    """Test render_pdf_stage, render_split_inspector, and render_pdf_viewer alias."""
    state = create_mock_state(sample_pdf_bytes)
    mock_render_pdf_page.return_value = b"\x89PNG fake image"
    col1, col2 = MagicMock(), MagicMock()
    col1.__enter__ = MagicMock(return_value=col1)
    col1.__exit__ = MagicMock(return_value=None)
    col2.__enter__ = MagicMock(return_value=col2)
    col2.__exit__ = MagicMock(return_value=None)
    mock_st.columns.return_value = [col1, col2]
    mock_st.number_input.return_value = 1
    mock_st.select_slider.return_value = 2.0
    mock_st.toggle.return_value = True
    mock_st.tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]
    mock_st.session_state = state

    with patch.object(st, "session_state", state):
        render_split_inspector()
        render_pdf_viewer()


@patch("pdf_classifier.components.qa_chat.query_ollama")
@patch("pdf_classifier.components.qa_chat.st")
def test_qa_chat_components(mock_st, mock_query_ollama, sample_pdf_bytes):
    """Test Q&A Chat helper functions and renders."""
    state = create_mock_state(sample_pdf_bytes)
    state.chat_suggestion = "What is the total due?"
    mock_st.session_state = state

    with patch.object(st, "session_state", state):
        _queue_suggestion()
        assert state.pending_query == "What is the total amount due on this document?"

        mock_st.chat_message.return_value.__enter__ = MagicMock()
        mock_st.chat_message.return_value.__exit__ = MagicMock()
        _render_message({"role": "assistant", "content": "hello", "latency_ms": 100}, 0)

        col1, col2 = MagicMock(), MagicMock()
        col1.__enter__ = MagicMock(return_value=col1)
        col1.__exit__ = MagicMock(return_value=None)
        col2.__enter__ = MagicMock(return_value=col2)
        col2.__exit__ = MagicMock(return_value=None)
        mock_st.columns.return_value = [col1, col2]
        mock_st.chat_input.return_value = "What is the date?"
        mock_query_ollama.return_value = "The date is 2023-01-01."

        render_qa_chat("llama3")
        render_chat_workspace("llama3")
        assert len(state.chat_history) >= 2


@patch("pdf_classifier.components.search_view.st")
def test_render_search_view(mock_st, sample_pdf_bytes):
    """Test render_search_view with and without query."""
    state = create_mock_state(sample_pdf_bytes)
    mock_st.session_state = state

    with patch.object(st, "session_state", state):
        mock_st.text_input.return_value = ""
        render_search_view()
        mock_st.info.assert_called_once()

        mock_st.text_input.return_value = "sample"
        render_search_view()
        assert mock_st.markdown.call_count >= 2


@patch("pdf_classifier.components.sidebar.query_ollama")
@patch("pdf_classifier.components.sidebar.extract_pdf_data")
def test_sidebar_and_extraction(mock_extract_pdf, mock_query_ollama, sample_pdf_bytes):
    """Test _run_extraction and render_sidebar."""
    state = create_mock_state(sample_pdf_bytes)
    uploaded_file = MagicMock()
    uploaded_file.getvalue.return_value = sample_pdf_bytes
    uploaded_file.name = "uploaded_doc.pdf"
    uploaded_file.size = 2048

    mock_extract_pdf.return_value = ("Extracted document text content", 2)
    mock_query_ollama.return_value = "Ollama generated summary"

    with patch.object(st, "session_state", state):
        _run_extraction(uploaded_file, "llama3", 0.1)
        assert state.uploaded_file_name == "uploaded_doc.pdf"
        assert state.ai_summary == "Ollama generated summary"
        assert "uploaded_doc.pdf" in state.recent_files

        mock_st_sidebar = MagicMock()
        mock_st_sidebar.file_uploader.return_value = uploaded_file
        mock_st_sidebar.text_input.return_value = "llama3"
        mock_st_sidebar.slider.return_value = 0.1
        mock_st_sidebar.number_input.return_value = 200
        mock_st_sidebar.segmented_control.return_value = "Summary"
        mock_st_sidebar.button.return_value = True
        mock_st_sidebar.session_state = state

        with patch("pdf_classifier.components.sidebar.st", mock_st_sidebar):
            model_name = render_sidebar()
            assert model_name == "llama3"


@patch("pdf_classifier.components.summary_view.st")
def test_render_summary_view(mock_st, sample_pdf_bytes):
    """Test render_summary_view."""
    state = create_mock_state(sample_pdf_bytes)
    mock_st.session_state = state

    with patch.object(st, "session_state", state):
        render_summary_view()
        mock_st.subheader.assert_called_once_with("Automated AI Intelligence Report")
        mock_st.markdown.assert_called_once()
