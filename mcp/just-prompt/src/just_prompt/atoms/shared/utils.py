"""Utility functions for just-prompt."""

from typing import Any


def split_provider_and_model(model_string: str) -> tuple[str, str]:
    """
    Split a model string into provider prefix and model name.

    Handles formats:
      - "provider:model"
      - "provider:model:suffix"  (suffix stays attached to model)

    Returns:
        (provider_prefix, model_with_optional_suffix)

    Examples:
        "openai:gpt-4o" -> ("openai", "gpt-4o")
        "o:gpt-4o" -> ("o", "gpt-4o")
        "openai:o4-mini:high" -> ("openai", "o4-mini:high")
        "anthropic:claude-opus-4-20250514:4k" -> ("anthropic", "claude-opus-4-20250514:4k")
    """
    parts = model_string.split(":", 2)
    if len(parts) < 2:
        raise ValueError(
            f"Invalid model string '{model_string}': expected 'provider:model'"
        )
    provider = parts[0]
    model = ":".join(parts[1:])
    return provider, model


def parse_thinking_suffix(model: str) -> tuple[str, Any]:
    """
    Extract thinking token budget or reasoning effort suffix from a model name.

    For Anthropic: ':1k', ':4k', ':8000' -> budget in tokens (int)
    For Gemini: ':1k', ':24576' -> budget in tokens (int)
    For OpenAI: ':low', ':medium', ':high' -> reasoning effort (str)

    Returns:
        (clean_model_name, budget_or_effort_or_None)
    """
    openai_efforts = {"low", "medium", "high"}
    parts = model.rsplit(":", 1)
    if len(parts) == 2:
        suffix = parts[1]
        # OpenAI reasoning effort strings
        if suffix in openai_efforts:
            return parts[0], suffix
        # k-notation (e.g. "4k" -> 4096)
        if suffix.endswith("k"):
            try:
                budget = int(suffix[:-1]) * 1024
                return parts[0], budget
            except ValueError:
                pass
        # Exact numeric (e.g. "8000")
        try:
            budget = int(suffix)
            return parts[0], budget
        except ValueError:
            pass
    return model, None
