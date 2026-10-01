"""Unit tests for text metrics calculations and search highlighter."""

from pdf_classifier.services.metrics_service import (
    compute_text_metrics,
    extract_entities,
    highlight_keywords,
)


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


def test_extract_entities():
    """Test extract_entities for extracting currencies and dates with limit."""
    text = (
        "Total due is $100.50 or €50.00 or £20.00. "
        "Alternative amounts: 100.00 USD, 50.00 EUR, 20.00 GBP. "
        "Duplicate amount $100.50. "
        "Dates: 2023-05-12, 05/12/2023, May 12, 2023, Jan 1, 2024. Duplicate date 2023-05-12."
    )
    entities = extract_entities(text, limit=3)
    assert len(entities["amounts"]) == 3
    assert "$100.50" in entities["amounts"]
    assert len(entities["dates"]) == 3
    assert "2023-05-12" in entities["dates"]
