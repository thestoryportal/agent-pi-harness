"""Google Gemini provider module for just-prompt."""

import os

from google import genai
from google.genai import types as genai_types

from just_prompt.atoms.shared.utils import parse_thinking_suffix

THINKING_MODELS = ["gemini-2.5-flash-preview-04-17"]


def prompt(text: str, model: str) -> str:
    """Send a prompt to a Gemini model.

    Supports thinking budget suffixes: ':1k' through ':24576'.
    Valid range: [0, 24576].
    """
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    clean_model, budget = parse_thinking_suffix(model)

    if (
        budget
        and isinstance(budget, int)
        and any(tm in clean_model for tm in THINKING_MODELS)
    ):
        budget = max(0, min(24576, budget))
        config = genai_types.GenerateContentConfig(
            thinking_config=genai_types.ThinkingConfig(
                thinking_budget=budget
            )
        )
        response = client.models.generate_content(
            model=clean_model, contents=text, config=config
        )
    else:
        response = client.models.generate_content(
            model=clean_model, contents=text
        )

    return response.text or ""


def list_models() -> list[str]:
    """List available Gemini models."""
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    models = client.models.list()
    return [m.name for m in models]
