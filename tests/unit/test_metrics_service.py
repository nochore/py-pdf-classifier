"""Unit tests for text metrics calculations and search highlighter."""

from pdf_classifier.services.metrics_service import compute_text_metrics, highlight_keywords


def test_compute_text_metrics_empty():
    """Test text metrics calculation for empty text."""
    metrics = compute_text_metrics("", 0)
    assert metrics["page_count"] == 0
    assert metrics["word_count"] == 0
    assert metrics["char_count"] == 0
    assert metrics["avg_word_length"] == 0.0
    assert metrics["reading_time_min"] == 0.0


def test_compute_text_metrics_sample():
    """Test text metrics calculation for sample text."""
    sample_text = (
        "This is a simple enterprise test document containing "
        "twenty words in total to test reading time calculations."
    )
    metrics = compute_text_metrics(sample_text, 1)
    assert metrics["page_count"] == 1
    assert metrics["word_count"] == 17
    assert metrics["char_count"] == len(sample_text)
    assert metrics["avg_word_length"] > 0
    assert metrics["reading_time_min"] == round(17 / 200, 1)


def test_highlight_keywords_empty():
    """Test highlight_keywords with empty or whitespace keyword."""
    text = "Sample document text."
    highlighted, matches = highlight_keywords(text, "  ")
    assert highlighted == text
    assert matches == 0


def test_highlight_keywords_matches():
    """Test highlight_keywords with matching keyword."""
    text = "Invoice #1001 for Invoice items."
    highlighted, matches = highlight_keywords(text, "invoice")
    assert matches == 2
    assert '<mark class="highlight-match" data-testid="search-match">Invoice</mark>' in highlighted
