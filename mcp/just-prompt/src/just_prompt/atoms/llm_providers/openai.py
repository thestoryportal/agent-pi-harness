"""OpenAI provider module for just-prompt."""

import os

from openai import OpenAI

from just_prompt.atoms.shared.utils import parse_thinking_suffix

O_SERIES_PREFIXES = ["o1", "o3", "o4", "o4-mini", "o3-mini", "o1-mini"]


def prompt(text: str, model: str) -> str:
    """Send a prompt to an OpenAI model.

    Supports reasoning effort suffixes for o-series models:
    ':low', ':medium', ':high'.
    """
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    clean_model, effort = parse_thinking_suffix(model)

    is_o_series = any(clean_model.startswith(m) for m in O_SERIES_PREFIXES)

    if effort and isinstance(effort, str) and is_o_series:
        try:
            response = client.responses.create(
                model=clean_model,
                reasoning={"effort": effort},
                input=text,
            )
            return response.output_text
        except (AttributeError, TypeError):
            # Fallback to chat completions if responses API unavailable
            response = client.chat.completions.create(
                model=clean_model,
                messages=[{"role": "user", "content": text}],
            )
            return response.choices[0].message.content or ""
    else:
        response = client.chat.completions.create(
            model=clean_model,
            messages=[{"role": "user", "content": text}],
        )
        return response.choices[0].message.content or ""


def list_models() -> list[str]:
    """List available OpenAI models."""
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    models = client.models.list()
    return [m.id for m in models.data]
