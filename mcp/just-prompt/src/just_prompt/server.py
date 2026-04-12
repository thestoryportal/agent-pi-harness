"""MCP server for just-prompt — unified multi-provider LLM interface."""

import json
import logging
import os

from mcp.server.fastmcp import FastMCP

from just_prompt.atoms.shared.validator import warn_missing_providers
from just_prompt.molecules.ceo_and_board_prompt import ceo_and_board as _ceo_and_board
from just_prompt.molecules.list_models import list_models as _list_models
from just_prompt.molecules.list_providers import list_providers as _list_providers
from just_prompt.molecules.prompt import prompt as _prompt
from just_prompt.molecules.prompt_from_file import (
    prompt_from_file as _prompt_from_file,
    prompt_from_file_to_file as _prompt_from_file_to_file,
)

logger = logging.getLogger(__name__)


def create_server(default_models: list[str]) -> FastMCP:
    """Create and configure the MCP server with all tools registered."""
    os.environ["JUST_PROMPT_DEFAULT_MODELS"] = ",".join(default_models)
    warn_missing_providers()

    mcp = FastMCP("just-prompt")

    @mcp.tool()
    def prompt(
        text: str,
        models_prefixed_by_provider: list[str] | None = None,
    ) -> str:
        """Send a prompt to multiple LLM models."""
        results = _prompt(text, models_prefixed_by_provider)
        return json.dumps(results, indent=2)

    @mcp.tool()
    def prompt_from_file(
        abs_file_path: str,
        models_prefixed_by_provider: list[str] | None = None,
    ) -> str:
        """Send a prompt from a file to multiple LLM models."""
        results = _prompt_from_file(abs_file_path, models_prefixed_by_provider)
        return json.dumps(results, indent=2)

    @mcp.tool()
    def prompt_from_file_to_file(
        abs_file_path: str,
        models_prefixed_by_provider: list[str] | None = None,
        abs_output_dir: str | None = None,
    ) -> str:
        """Send a prompt from a file to models and save responses as markdown."""
        results = _prompt_from_file_to_file(
            abs_file_path, models_prefixed_by_provider, abs_output_dir
        )
        return json.dumps(results, indent=2)

    @mcp.tool()
    def ceo_and_board(
        abs_file_path: str,
        models_prefixed_by_provider: list[str] | None = None,
        abs_output_dir: str | None = None,
        ceo_model: str = "openai:o3",
    ) -> str:
        """Board member models respond, CEO synthesizes a final decision."""
        return _ceo_and_board(
            abs_file_path,
            models_prefixed_by_provider,
            abs_output_dir,
            ceo_model,
        )

    @mcp.tool()
    def list_providers() -> str:
        """List all available LLM providers."""
        results = _list_providers()
        return json.dumps(results, indent=2)

    @mcp.tool()
    def list_models(provider: str) -> str:
        """List all available models for a specific provider."""
        results = _list_models(provider)
        return json.dumps(results, indent=2)

    return mcp
