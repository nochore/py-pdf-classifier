"""Ollama API integration service."""

import os

import requests


def query_ollama(
    prompt: str,
    model: str = "llama3",
    system_prompt: str = "",
    host: str | None = None,
    timeout: int = 60,
) -> str:
    """Query local Ollama instance for text generation."""
    if host is None:
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

    url = f"{host.rstrip('/')}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "system": system_prompt,
        "stream": False,
    }

    try:
        response = requests.post(url, json=payload, timeout=timeout)
        response.raise_for_status()
        return str(response.json().get("response", "No response received."))
    except requests.exceptions.ConnectionError:
        return (
            "Error: Could not connect to Ollama service. "
            "Ensure local engine is operational (ollama serve)."
        )
    except Exception as e:
        return f"Error: {str(e)}"
