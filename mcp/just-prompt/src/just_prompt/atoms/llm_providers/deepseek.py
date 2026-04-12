"""DeepSeek provider module for just-prompt."""

import os

from openai import OpenAI

DEEPSEEK_BASE_URL = "https://api.deepseek.com"


def prompt(text: str, model: str) -> str:
    """Send a prompt to a DeepSeek model."""
    client = OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url=DEEPSEEK_BASE_URL,
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": text}],
    )
    return response.choices[0].message.content or ""


def list_models() -> list[str]:
    """List available DeepSeek models."""
    client = OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url=DEEPSEEK_BASE_URL,
    )
    models = client.models.list()
    return [m.id for m in models.data]
