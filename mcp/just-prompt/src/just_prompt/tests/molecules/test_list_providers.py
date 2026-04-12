"""Tests for list_providers molecule."""

from just_prompt.molecules.list_providers import list_providers


def test_list_providers_returns_all_six():
    """Returns all 6 provider entries."""
    result = list_providers()
    assert len(result["providers"]) == 6
    names = [p["name"] for p in result["providers"]]
    assert "openai" in names
    assert "anthropic" in names
    assert "gemini" in names
    assert "groq" in names
    assert "deepseek" in names
    assert "ollama" in names


def test_list_providers_has_aliases():
    """Each provider has correct aliases."""
    result = list_providers()
    anthropic_entry = next(
        p for p in result["providers"] if p["name"] == "anthropic"
    )
    assert "a" in anthropic_entry["aliases"]
    assert "anthropic" in anthropic_entry["aliases"]


def test_list_providers_has_availability():
    """Each provider entry has an 'available' boolean."""
    result = list_providers()
    for provider in result["providers"]:
        assert "available" in provider
        assert isinstance(provider["available"], bool)
