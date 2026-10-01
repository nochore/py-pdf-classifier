"""Unit tests for PDF extraction and rendering service."""

import pymupdf
import pytest

from pdf_classifier.services.pdf_service import extract_pdf_data, render_pdf_page_cached


@pytest.fixture
def sample_pdf_bytes() -> bytes:
    """Generate in-memory sample PDF bytes for testing."""
    doc = pymupdf.open()
    page1 = doc.new_page()
    page1.insert_text((50, 50), "Hello World PDF Page 1")
    page2 = doc.new_page()
    page2.insert_text((50, 50), "Financial Report Invoice Page 2")
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def test_extract_pdf_data_empty():
    """Test extract_pdf_data with empty input."""
    text, page_count = extract_pdf_data(b"")
    assert text == ""
    assert page_count == 0


def test_extract_pdf_data_valid(sample_pdf_bytes: bytes):
    """Test extract_pdf_data with valid PDF bytes."""
    text, page_count = extract_pdf_data(sample_pdf_bytes)
    assert page_count == 2
    assert "Hello World PDF Page 1" in text
    assert "Financial Report Invoice Page 2" in text


def test_render_pdf_page_cached_empty():
    """Test render_pdf_page_cached with empty bytes."""
    img_bytes = render_pdf_page_cached(b"", 0, 1.0)
    assert img_bytes == b""


def test_render_pdf_page_cached_valid(sample_pdf_bytes: bytes):
    """Test render_pdf_page_cached returns PNG image bytes."""
    img_bytes = render_pdf_page_cached(sample_pdf_bytes, 0, 1.0)
    assert isinstance(img_bytes, bytes)
    assert len(img_bytes) > 0
    # Check PNG signature
    assert img_bytes[:4] == b"\x89PNG"


def test_render_pdf_page_cached_out_of_bounds(sample_pdf_bytes: bytes):
    """Test render_pdf_page_cached with out of bounds page index."""
    img_bytes = render_pdf_page_cached(sample_pdf_bytes, 99, 1.0)
    assert img_bytes == b""


def test_render_pdf_page_cached_with_highlights(sample_pdf_bytes: bytes):
    """Test render_pdf_page_cached with highlight overlays."""
    highlights = (("Hello", "amount"), ("World", "date"), ("PDF", "other"))
    img_bytes = render_pdf_page_cached(sample_pdf_bytes, 0, 1.0, highlights=highlights)
    assert isinstance(img_bytes, bytes)
    assert len(img_bytes) > 0
    assert img_bytes[:4] == b"\x89PNG"
