"""Tests for prompt molecule."""

from unittest.mock import patch

from just_prompt.molecules.prompt import prompt


@patch("just_prompt.molecules.prompt.ModelRouter")
def test_prompt_single_model(mock_router):
    """Single model dispatch returns correct result."""
    mock_router.route_prompt.return_value = "mocked response"

    result = prompt("hello", ["openai:gpt-4o"])
    assert result == {"openai:gpt-4o": "mocked response"}
    mock_router.route_prompt.assert_called_once_with("openai:gpt-4o", "hello")


@patch("just_prompt.molecules.prompt.ModelRouter")
def test_prompt_multiple_models(mock_router):
    """Multiple models dispatched in parallel."""

    def side_effect(model, text):
        return f"response from {model}"

    mock_router.route_prompt.side_effect = side_effect

    result = prompt(
        "hello", ["openai:gpt-4o", "anthropic:claude-sonnet-4-20250514"]
    )
    assert "openai:gpt-4o" in result
    assert "anthropic:claude-sonnet-4-20250514" in result
    assert result["openai:gpt-4o"] == "response from openai:gpt-4o"


@patch.dict(
    "os.environ",
    {"JUST_PROMPT_DEFAULT_MODELS": "anthropic:claude-sonnet-4-20250514"},
)
@patch("just_prompt.molecules.prompt.ModelRouter")
def test_prompt_uses_default_models(mock_router):
    """Falls back to JUST_PROMPT_DEFAULT_MODELS env var."""
    mock_router.route_prompt.return_value = "default response"

    result = prompt("hello")
    assert "anthropic:claude-sonnet-4-20250514" in result


@patch("just_prompt.molecules.prompt.ModelRouter")
def test_prompt_error_captured(mock_router):
    """Errors from models are captured, not raised."""
    mock_router.route_prompt.side_effect = RuntimeError("API down")

    result = prompt("hello", ["openai:gpt-4o"])
    assert "openai:gpt-4o" in result
    assert result["openai:gpt-4o"].startswith("ERROR:")
