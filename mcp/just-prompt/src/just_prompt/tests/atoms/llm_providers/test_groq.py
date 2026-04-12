"""Tests for Groq provider module."""

from unittest.mock import MagicMock, patch

from just_prompt.atoms.llm_providers import groq as groq_mod


@patch.dict("os.environ", {"GROQ_API_KEY": "test-key"})
@patch("just_prompt.atoms.llm_providers.groq.Groq")
def test_prompt_basic(mock_groq_cls):
    """Basic prompt to Groq."""
    mock_client = MagicMock()
    mock_groq_cls.return_value = mock_client

    mock_message = MagicMock()
    mock_message.content = "Fast response"
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response

    result = groq_mod.prompt("Say hello", "llama-3.1-70b-versatile")
    assert result == "Fast response"


@patch.dict("os.environ", {"GROQ_API_KEY": "test-key"})
@patch("just_prompt.atoms.llm_providers.groq.Groq")
def test_list_models(mock_groq_cls):
    """list_models returns model IDs."""
    mock_client = MagicMock()
    mock_groq_cls.return_value = mock_client

    m1 = MagicMock()
    m1.id = "llama-3.1-70b-versatile"
    mock_client.models.list.return_value = MagicMock(data=[m1])

    result = groq_mod.list_models()
    assert result == ["llama-3.1-70b-versatile"]
