"""Tests for Gemini provider module."""

from unittest.mock import MagicMock, patch

from just_prompt.atoms.llm_providers import gemini as gemini_mod


@patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"})
@patch("just_prompt.atoms.llm_providers.gemini.genai")
def test_prompt_basic(mock_genai):
    """Basic prompt without thinking budget."""
    mock_client = MagicMock()
    mock_genai.Client.return_value = mock_client

    mock_response = MagicMock()
    mock_response.text = "Hello from Gemini"
    mock_client.models.generate_content.return_value = mock_response

    result = gemini_mod.prompt("Say hello", "gemini-2.5-pro")
    assert result == "Hello from Gemini"
    call_kwargs = mock_client.models.generate_content.call_args[1]
    assert call_kwargs["model"] == "gemini-2.5-pro"
    assert "config" not in call_kwargs


@patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"})
@patch("just_prompt.atoms.llm_providers.gemini.genai")
def test_prompt_with_thinking(mock_genai):
    """Thinking model with budget suffix triggers thinking config."""
    mock_client = MagicMock()
    mock_genai.Client.return_value = mock_client

    mock_response = MagicMock()
    mock_response.text = "Thoughtful Gemini"
    mock_client.models.generate_content.return_value = mock_response

    result = gemini_mod.prompt(
        "Think hard", "gemini-2.5-flash-preview-04-17:8k"
    )
    assert result == "Thoughtful Gemini"
    call_kwargs = mock_client.models.generate_content.call_args[1]
    assert call_kwargs["model"] == "gemini-2.5-flash-preview-04-17"
    assert "config" in call_kwargs


@patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"})
@patch("just_prompt.atoms.llm_providers.gemini.genai")
def test_list_models(mock_genai):
    """list_models returns model names."""
    mock_client = MagicMock()
    mock_genai.Client.return_value = mock_client

    m1 = MagicMock()
    m1.name = "gemini-2.5-pro"
    m2 = MagicMock()
    m2.name = "gemini-2.5-flash"
    mock_client.models.list.return_value = [m1, m2]

    result = gemini_mod.list_models()
    assert result == ["gemini-2.5-pro", "gemini-2.5-flash"]
