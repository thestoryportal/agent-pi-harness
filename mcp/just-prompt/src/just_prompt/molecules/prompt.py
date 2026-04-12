"""Send a prompt to multiple LLM models in parallel."""

import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from just_prompt.atoms.shared.model_router import ModelRouter

logger = logging.getLogger(__name__)


def get_default_models() -> list[str]:
    """Get default models from environment variable."""
    raw = os.environ.get(
        "JUST_PROMPT_DEFAULT_MODELS", "anthropic:claude-sonnet-4-20250514"
    )
    return [m.strip() for m in raw.split(",") if m.strip()]


def prompt(
    text: str,
    models_prefixed_by_provider: list[str] | None = None,
) -> dict[str, str]:
    """Send a prompt to multiple LLM models in parallel.

    Args:
        text: The prompt text.
        models_prefixed_by_provider: List of "provider:model[:suffix]" strings.
            Falls back to JUST_PROMPT_DEFAULT_MODELS env var.

    Returns:
        Dict mapping model string to response text.
    """
    models = models_prefixed_by_provider or get_default_models()
    results: dict[str, str] = {}

    with ThreadPoolExecutor(max_workers=len(models)) as executor:
        futures = {
            executor.submit(ModelRouter.route_prompt, model, text): model
            for model in models
        }
        for future in as_completed(futures):
            model = futures[future]
            try:
                results[model] = future.result()
            except Exception as e:
                logger.error("Error from model %s: %s", model, e)
                results[model] = f"ERROR: {e}"

    return results
