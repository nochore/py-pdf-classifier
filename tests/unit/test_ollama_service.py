"""Unit tests for Ollama API interaction service."""

from unittest.mock import MagicMock, patch

import requests

from pdf_classifier.services.ollama_service import query_ollama


@patch("pdf_classifier.services.ollama_service.requests.post")
def test_query_ollama_success(mock_post):
    """Test query_ollama returns API response content on success."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "Classified as Financial Report"}
    mock_post.return_value = mock_response

    result = query_ollama(prompt="Classify this doc", model="llama3")
    assert result == "Classified as Financial Report"
    mock_post.assert_called_once()


@patch("pdf_classifier.services.ollama_service.requests.post")
def test_query_ollama_connection_error(mock_post):
    """Test query_ollama handles connection error gracefully."""
    mock_post.side_effect = requests.exceptions.ConnectionError("Connection refused")

    result = query_ollama(prompt="Classify this doc", model="llama3")
    assert "Could not connect to Ollama service" in result


@patch("pdf_classifier.services.ollama_service.requests.post")
def test_query_ollama_generic_exception(mock_post):
    """Test query_ollama handles generic exception."""
    mock_post.side_effect = Exception("HTTP 500 Internal Error")

    result = query_ollama(prompt="Classify this doc", model="llama3")
    assert "Error: HTTP 500 Internal Error" in result
