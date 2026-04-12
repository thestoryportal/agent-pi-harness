"""Tests for Anthropic provider module."""

from unittest.mock import MagicMock, patch

from just_prompt.atoms.llm_providers import anthropic as anthropic_mod


@patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"})
@patch("just_prompt.atoms.llm_providers.anthropic.Anthropic")
def test_prompt_basic(mock_anthropic_cls):
    """Basic prompt without thinking tokens."""
    mock_client = MagicMock()
    mock_anthropic_cls.return_value = mock_client

    text_block = MagicMock()
    text_block.type = "text"
    text_block.text = "Hello from Claude"
    mock_response = MagicMock()
    mock_response.content = [text_block]
    mock_client.messages.create.return_value = mock_response

    result = anthropic_mod.prompt("Say hello", "claude-sonnet-4-20250514")
    assert result == "Hello from Claude"
    mock_client.messages.create.assert_called_once()
    call_kwargs = mock_client.messages.create.call_args[1]
    assert call_kwargs["model"] == "claude-sonnet-4-20250514"
    assert "thinking" not in call_kwargs


@patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"})
@patch("just_prompt.atoms.llm_providers.anthropic.Anthropic")
def test_prompt_with_thinking(mock_anthropic_cls):
    """Prompt with thinking token suffix triggers extended thinking."""
    mock_client = MagicMock()
    mock_anthropic_cls.return_value = mock_client

    text_block = MagicMock()
    text_block.type = "text"
    text_block.text = "Thoughtful response"
    mock_response = MagicMock()
    mock_response.content = [text_block]
    mock_client.messages.create.return_value = mock_response

    result = anthropic_mod.prompt("Think hard", "claude-opus-4-20250514:4k")
    assert result == "Thoughtful response"
    call_kwargs = mock_client.messages.create.call_args[1]
    assert call_kwargs["model"] == "claude-opus-4-20250514"
    assert call_kwargs["thinking"] == {
        "type": "enabled",
        "budget_tokens": 4096,
    }


@patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"})
@patch("just_prompt.atoms.llm_providers.anthropic.Anthropic")
def test_prompt_thinking_clamped(mock_anthropic_cls):
    """Thinking budget is clamped to [1024, 16000]."""
    mock_client = MagicMock()
    mock_anthropic_cls.return_value = mock_client

    text_block = MagicMock()
    text_block.type = "text"
    text_block.text = "ok"
    mock_response = MagicMock()
    mock_response.content = [text_block]
    mock_client.messages.create.return_value = mock_response

    # Budget too small -> clamped to 1024
    anthropic_mod.prompt("test", "claude-opus-4-20250514:100")
    call_kwargs = mock_client.messages.create.call_args[1]
    assert call_kwargs["thinking"]["budget_tokens"] == 1024


@patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"})
@patch("just_prompt.atoms.llm_providers.anthropic.Anthropic")
def test_list_models(mock_anthropic_cls):
    """list_models returns model IDs."""
    mock_client = MagicMock()
    mock_anthropic_cls.return_value = mock_client

    m1 = MagicMock()
    m1.id = "claude-sonnet-4-20250514"
    m2 = MagicMock()
    m2.id = "claude-haiku-3-5"
    mock_client.models.list.return_value = MagicMock(data=[m1, m2])

    result = anthropic_mod.list_models()
    assert result == ["claude-sonnet-4-20250514", "claude-haiku-3-5"]
