"""
Model router for dispatching requests to the appropriate provider.
"""

import importlib
import logging
import os

from .data_types import ModelProviders
from .utils import split_provider_and_model

logger = logging.getLogger(__name__)


class ModelRouter:
    """
    Routes requests to the appropriate provider based on the model string.
    """

    # Allowlisted provider names for importlib safety
    _VALID_PROVIDERS = frozenset(p.full_name for p in ModelProviders)

    @staticmethod
    def validate_and_correct_model(provider_name: str, model_name: str) -> str:
        """
        Validate a model name against available models for a provider, and correct it if needed.

        Args:
            provider_name: Provider name (full name)
            model_name: Model name to validate and potentially correct

        Returns:
            Validated and potentially corrected model name
        """
        if provider_name not in ModelRouter._VALID_PROVIDERS:
            raise ValueError(f"Unknown provider: {provider_name}")

        # Early return for our thinking token models to bypass validation
        thinking_models = [
            "claude-3-7-sonnet-20250219",
            "claude-opus-4-20250514",
            "claude-sonnet-4-20250514",
            "gemini-2.5-flash-preview-04-17",
        ]
        if any(thinking_model in model_name for thinking_model in thinking_models):
            return model_name

        try:
            # Import the provider module
            provider_module_name = (
                f"just_prompt.atoms.llm_providers.{provider_name}"
            )
            provider_module = importlib.import_module(provider_module_name)

            # Get available models
            available_models = provider_module.list_models()

            # Check if model is in available models
            if model_name in available_models:
                return model_name

            # Model needs correction - use the default correction model
            correction_model = os.environ.get(
                "CORRECTION_MODEL", "anthropic:claude-3-7-sonnet-20250219"
            )

            # Use magic model correction
            corrected_model = ModelRouter.magic_model_correction(
                provider_name, model_name, correction_model
            )

            if corrected_model != model_name:
                logger.info(
                    "Corrected model name from '%s' to '%s' for provider '%s'",
                    model_name,
                    corrected_model,
                    provider_name,
                )
                return corrected_model

            return model_name
        except Exception as e:
            logger.warning(
                "Error validating model '%s' for provider '%s': %s",
                model_name,
                provider_name,
                e,
            )
            return model_name

    @staticmethod
    def route_prompt(model_string: str, text: str) -> str:
        """
        Route a prompt to the appropriate provider.

        Args:
            model_string: String in format "provider:model"
            text: The prompt text

        Returns:
            Response from the model
        """
        provider_prefix, model = split_provider_and_model(model_string)
        provider = ModelProviders.from_name(provider_prefix)

        if not provider:
            raise ValueError(f"Unknown provider prefix: {provider_prefix}")

        # Validate and potentially correct the model name
        validated_model = ModelRouter.validate_and_correct_model(
            provider.full_name, model
        )

        # Import the appropriate provider module
        try:
            module_name = (
                f"just_prompt.atoms.llm_providers.{provider.full_name}"
            )
            provider_module = importlib.import_module(module_name)

            # Call the prompt function
            return provider_module.prompt(text, validated_model)
        except ImportError as e:
            logger.error("Failed to import provider module: %s", e)
            raise ValueError(
                f"Provider not available: {provider.full_name}"
            ) from e
        except Exception as e:
            logger.error(
                "Error routing prompt to %s: %s", provider.full_name, e
            )
            raise

    @staticmethod
    def route_list_models(provider_name: str) -> list[str]:
        """
        Route a list_models request to the appropriate provider.

        Args:
            provider_name: Provider name (full or short)

        Returns:
            List of model names
        """
        provider = ModelProviders.from_name(provider_name)

        if not provider:
            raise ValueError(f"Unknown provider: {provider_name}")

        # Import the appropriate provider module
        try:
            module_name = (
                f"just_prompt.atoms.llm_providers.{provider.full_name}"
            )
            provider_module = importlib.import_module(module_name)

            # Call the list_models function
            return provider_module.list_models()
        except ImportError as e:
            logger.error("Failed to import provider module: %s", e)
            raise ValueError(
                f"Provider not available: {provider.full_name}"
            ) from e
        except Exception as e:
            logger.error(
                "Error listing models for %s: %s", provider.full_name, e
            )
            raise

    @staticmethod
    def magic_model_correction(
        provider: str, model: str, correction_model: str
    ) -> str:
        """
        Correct a model name using a correction AI model if needed.

        Args:
            provider: Provider name
            model: Original model name
            correction_model: Model to use for the correction llm prompt

        Returns:
            Corrected model name
        """
        provider_module_name = f"just_prompt.atoms.llm_providers.{provider}"

        try:
            provider_module = importlib.import_module(provider_module_name)
            available_models = provider_module.list_models()

            # If model is already in available models, no correction needed
            if model in available_models:
                logger.info("Using %s and %s", provider, model)
                return model

            # Model needs correction - use correction model to correct it
            correction_provider, correction_model_name = (
                split_provider_and_model(correction_model)
            )
            correction_provider_enum = ModelProviders.from_name(
                correction_provider
            )

            if not correction_provider_enum:
                logger.warning(
                    "Invalid correction model provider: %s, skipping correction",
                    correction_provider,
                )
                return model

            correction_module_name = f"just_prompt.atoms.llm_providers.{correction_provider_enum.full_name}"
            correction_module = importlib.import_module(
                correction_module_name
            )

            # Build prompt for the correction model
            prompt = f"""
Given a user-provided model name "{model}" for the provider "{provider}", and the list of actual available models below,
return the closest matching model name from the available models list.
Only return the exact model name, nothing else.

Available models: {', '.join(available_models)}
"""
            # Get correction from correction model
            corrected_model = correction_module.prompt(
                prompt, correction_model_name
            ).strip()

            # Verify the corrected model exists in the available models
            if corrected_model in available_models:
                logger.info("correction_model: %s", correction_model)
                logger.info(
                    "models_prefixed_by_provider: %s:%s", provider, model
                )
                logger.info("corrected_model: %s", corrected_model)
                return corrected_model
            else:
                logger.warning(
                    "Corrected model %s not found in available models",
                    corrected_model,
                )
                return model

        except Exception as e:
            logger.error("Error in model correction: %s", e)
            return model
