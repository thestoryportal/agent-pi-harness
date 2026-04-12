"""Ollama provider module for just-prompt."""

import os

import ollama as ollama_sdk


def _get_client():
    """Create Ollama client with configured host."""
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    return ollama_sdk.Client(host=host)


def prompt(text: str, model: str) -> str:
    """Send a prompt to an Ollama model."""
    client = _get_client()
    response = client.chat(
        model=model,
        messages=[{"role": "user", "content": text}],
    )
    return response.message.content or ""


def list_models() -> list[str]:
    """List available Ollama models."""
    client = _get_client()
    models = client.list()
    return [m.model for m in models.models]
