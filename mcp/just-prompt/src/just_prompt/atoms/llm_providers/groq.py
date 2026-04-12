"""Groq provider module for just-prompt."""

import os

from groq import Groq


def prompt(text: str, model: str) -> str:
    """Send a prompt to a Groq model."""
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": text}],
    )
    return response.choices[0].message.content or ""


def list_models() -> list[str]:
    """List available Groq models."""
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    models = client.models.list()
    return [m.id for m in models.data]
