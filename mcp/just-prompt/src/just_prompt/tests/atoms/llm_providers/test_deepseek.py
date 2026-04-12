"""Tests for DeepSeek provider module."""

from unittest.mock import MagicMock, patch

from just_prompt.atoms.llm_providers import deepseek as deepseek_mod


@patch.dict("os.environ", {"DEEPSEEK_API_KEY": "test-key"})
@patch("just_prompt.atoms.llm_providers.deepseek.OpenAI")
def test_prompt_basic(mock_openai_cls):
    """Basic prompt uses OpenAI SDK with DeepSeek base URL."""
    mock_client = MagicMock()
    mock_openai_cls.return_value = mock_client

    mock_message = MagicMock()
    mock_message.content = "DeepSeek response"
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response

    result = deepseek_mod.prompt("Say hello", "deepseek-chat")
    assert result == "DeepSeek response"

    # Verify DeepSeek base URL was used
    call_kwargs = mock_openai_cls.call_args[1]
    assert call_kwargs["base_url"] == "https://api.deepseek.com"


@patch.dict("os.environ", {"DEEPSEEK_API_KEY": "test-key"})
@patch("just_prompt.atoms.llm_providers.deepseek.OpenAI")
def test_list_models(mock_openai_cls):
    """list_models returns model IDs."""
    mock_client = MagicMock()
    mock_openai_cls.return_value = mock_client

    m1 = MagicMock()
    m1.id = "deepseek-chat"
    mock_client.models.list.return_value = MagicMock(data=[m1])

    result = deepseek_mod.list_models()
    assert result == ["deepseek-chat"]
