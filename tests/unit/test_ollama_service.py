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


@patch("pdf_classifier.services.ollama_service.requests.post")
def test_query_ollama_options_and_host(mock_post, monkeypatch):
    """Test query_ollama with custom host, temperature and env var fallback."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "Custom host response"}
    mock_post.return_value = mock_response

    # Test custom host parameter & temperature option
    res = query_ollama(
        prompt="Hi", model="m1", host="http://custom-host:11434/", temperature=0.7
    )
    assert res == "Custom host response"
    args, kwargs = mock_post.call_args
    assert args[0] == "http://custom-host:11434/api/generate"
    assert kwargs["json"]["options"] == {"temperature": 0.7}

    # Test environment variable fallback when host is None
    monkeypatch.setenv("OLLAMA_HOST", "http://env-host:11434")
    query_ollama(prompt="Hi", model="m1")
    args, kwargs = mock_post.call_args
    assert args[0] == "http://env-host:11434/api/generate"
