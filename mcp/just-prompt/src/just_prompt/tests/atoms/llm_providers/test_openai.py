"""Tests for OpenAI provider module."""

from unittest.mock import MagicMock, patch

from just_prompt.atoms.llm_providers import openai as openai_mod


@patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
@patch("just_prompt.atoms.llm_providers.openai.OpenAI")
def test_prompt_basic(mock_openai_cls):
    """Basic prompt without reasoning effort."""
    mock_client = MagicMock()
    mock_openai_cls.return_value = mock_client

    mock_message = MagicMock()
    mock_message.content = "Hello from GPT"
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response

    result = openai_mod.prompt("Say hello", "gpt-4o")
    assert result == "Hello from GPT"
    call_kwargs = mock_client.chat.completions.create.call_args[1]
    assert call_kwargs["model"] == "gpt-4o"


@patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
@patch("just_prompt.atoms.llm_providers.openai.OpenAI")
def test_prompt_with_reasoning(mock_openai_cls):
    """O-series model with reasoning effort uses responses API."""
    mock_client = MagicMock()
    mock_openai_cls.return_value = mock_client

    mock_response = MagicMock()
    mock_response.output_text = "Reasoned response"
    mock_client.responses.create.return_value = mock_response

    result = openai_mod.prompt("Think hard", "o3:high")
    assert result == "Reasoned response"
    call_kwargs = mock_client.responses.create.call_args[1]
    assert call_kwargs["model"] == "o3"
    assert call_kwargs["reasoning"] == {"effort": "high"}


@patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
@patch("just_prompt.atoms.llm_providers.openai.OpenAI")
def test_prompt_reasoning_fallback(mock_openai_cls):
    """Falls back to chat completions if responses API fails."""
    mock_client = MagicMock()
    mock_openai_cls.return_value = mock_client

    mock_client.responses.create.side_effect = AttributeError(
        "no responses API"
    )
    mock_message = MagicMock()
    mock_message.content = "Fallback response"
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response

    result = openai_mod.prompt("Think", "o4-mini:low")
    assert result == "Fallback response"


@patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
@patch("just_prompt.atoms.llm_providers.openai.OpenAI")
def test_list_models(mock_openai_cls):
    """list_models returns model IDs."""
    mock_client = MagicMock()
    mock_openai_cls.return_value = mock_client

    m1 = MagicMock()
    m1.id = "gpt-4o"
    m2 = MagicMock()
    m2.id = "gpt-4o-mini"
    mock_client.models.list.return_value = MagicMock(data=[m1, m2])

    result = openai_mod.list_models()
    assert result == ["gpt-4o", "gpt-4o-mini"]
