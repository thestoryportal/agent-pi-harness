"""List all available LLM providers."""

from just_prompt.atoms.shared.data_types import ModelProviders
from just_prompt.atoms.shared.validator import check_available_providers


def list_providers() -> dict:
    """List all available LLM providers with aliases and availability.

    Returns:
        Dict with provider info and which API keys are configured.
    """
    availability = check_available_providers()
    providers = []
    for provider in ModelProviders:
        providers.append(
            {
                "name": provider.full_name,
                "aliases": provider.aliases,
                "available": availability.get(provider.full_name, False),
            }
        )
    return {"providers": providers}
