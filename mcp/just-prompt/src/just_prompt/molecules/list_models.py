"""List models for a specific LLM provider."""

from just_prompt.atoms.shared.model_router import ModelRouter


def list_models(provider: str) -> list[str]:
    """List all available models for a specific provider.

    Args:
        provider: Provider name or short alias (e.g., 'openai' or 'o').

    Returns:
        List of model ID strings.
    """
    return ModelRouter.route_list_models(provider)
