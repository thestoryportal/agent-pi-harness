"""Tests for Ollama provider module."""

from unittest.mock import MagicMock, patch

from just_prompt.atoms.llm_providers import ollama as ollama_mod


@patch.dict(
    "os.environ", {"OLLAMA_HOST": "http://localhost:11434"}, clear=False
)
@patch("just_prompt.atoms.llm_providers.ollama.ollama_sdk")
def test_prompt_basic(mock_ollama_sdk):
    """Basic prompt to Ollama."""
    mock_client = MagicMock()
    mock_ollama_sdk.Client.return_value = mock_client

    mock_response = MagicMock()
    mock_response.message.content = "Local LLM response"
    mock_client.chat.return_value = mock_response

    result = ollama_mod.prompt("Say hello", "llama3.1")
    assert result == "Local LLM response"
    mock_client.chat.assert_called_once()


@patch.dict(
    "os.environ", {"OLLAMA_HOST": "http://localhost:11434"}, clear=False
)
@patch("just_prompt.atoms.llm_providers.ollama.ollama_sdk")
def test_list_models(mock_ollama_sdk):
    """list_models returns model names."""
    mock_client = MagicMock()
    mock_ollama_sdk.Client.return_value = mock_client

    m1 = MagicMock()
    m1.model = "llama3.1"
    m2 = MagicMock()
    m2.model = "mistral"
    mock_client.list.return_value = MagicMock(models=[m1, m2])

    result = ollama_mod.list_models()
    assert result == ["llama3.1", "mistral"]
