"""Provider availability validation."""

import logging
import os

logger = logging.getLogger(__name__)

PROVIDER_ENV_VARS = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "gemini": "GEMINI_API_KEY",
    "groq": "GROQ_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "ollama": None,  # Ollama uses OLLAMA_HOST, not an API key
}


def check_available_providers() -> dict[str, bool]:
    """Return dict of provider -> bool (key present)."""
    result = {}
    for provider, env_var in PROVIDER_ENV_VARS.items():
        if env_var is None:
            host = os.environ.get("OLLAMA_HOST", "")
            result[provider] = bool(host)
        else:
            result[provider] = bool(os.environ.get(env_var))
    return result


def warn_missing_providers():
    """Log a warning for each provider with no API key configured."""
    available = check_available_providers()
    for provider, is_available in available.items():
        if is_available:
            logger.info("Provider '%s' available", provider)
        else:
            logger.warning(
                "Provider '%s' unavailable: missing environment variable", provider
            )
