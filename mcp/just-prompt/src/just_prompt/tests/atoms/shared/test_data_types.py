"""Tests for shared data types."""

from just_prompt.atoms.shared.data_types import ModelProviders


def test_from_name_short():
    """Short alias resolves to correct provider."""
    assert ModelProviders.from_name("o") == ModelProviders.OPENAI
    assert ModelProviders.from_name("a") == ModelProviders.ANTHROPIC
    assert ModelProviders.from_name("g") == ModelProviders.GEMINI
    assert ModelProviders.from_name("q") == ModelProviders.GROQ
    assert ModelProviders.from_name("d") == ModelProviders.DEEPSEEK
    assert ModelProviders.from_name("l") == ModelProviders.OLLAMA


def test_from_name_long():
    """Full name resolves to correct provider."""
    assert ModelProviders.from_name("openai") == ModelProviders.OPENAI
    assert ModelProviders.from_name("anthropic") == ModelProviders.ANTHROPIC
    assert ModelProviders.from_name("gemini") == ModelProviders.GEMINI


def test_from_name_unknown():
    """Unknown name returns None."""
    assert ModelProviders.from_name("xyz") is None
    assert ModelProviders.from_name("") is None


def test_full_name_attribute():
    """Each provider has correct full_name."""
    assert ModelProviders.OPENAI.full_name == "openai"
    assert ModelProviders.ANTHROPIC.full_name == "anthropic"
    assert ModelProviders.GEMINI.full_name == "gemini"
    assert ModelProviders.GROQ.full_name == "groq"
    assert ModelProviders.DEEPSEEK.full_name == "deepseek"
    assert ModelProviders.OLLAMA.full_name == "ollama"


def test_all_names():
    """all_names returns all six provider names."""
    names = ModelProviders.all_names()
    assert len(names) == 6
    assert "openai" in names
    assert "anthropic" in names
