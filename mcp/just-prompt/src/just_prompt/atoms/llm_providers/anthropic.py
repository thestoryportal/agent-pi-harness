"""Anthropic provider module for just-prompt."""

import os

from anthropic import Anthropic

from just_prompt.atoms.shared.utils import parse_thinking_suffix

THINKING_MODELS = [
    "claude-3-7-sonnet-20250219",
    "claude-opus-4-20250514",
    "claude-sonnet-4-20250514",
]


def prompt(text: str, model: str) -> str:
    """Send a prompt to an Anthropic model.

    Supports thinking token suffixes: ':1k' through ':8000' for budget_tokens.
    Valid range: [1024, 16000].
    """
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    clean_model, budget = parse_thinking_suffix(model)

    if (
        budget
        and isinstance(budget, int)
        and any(tm in clean_model for tm in THINKING_MODELS)
    ):
        budget = max(1024, min(16000, budget))
        response = client.messages.create(
            model=clean_model,
            max_tokens=budget + 1000,
            thinking={"type": "enabled", "budget_tokens": budget},
            messages=[{"role": "user", "content": text}],
        )
    else:
        response = client.messages.create(
            model=clean_model,
            max_tokens=8096,
            messages=[{"role": "user", "content": text}],
        )

    for block in response.content:
        if block.type == "text":
            return block.text
    return ""


def list_models() -> list[str]:
    """List available Anthropic models."""
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    models = client.models.list()
    return [m.id for m in models.data]
