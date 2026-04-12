"""Tests for utility functions."""

import pytest

from just_prompt.atoms.shared.utils import parse_thinking_suffix, split_provider_and_model


def test_split_basic():
    """Basic provider:model split."""
    assert split_provider_and_model("openai:gpt-4o") == ("openai", "gpt-4o")


def test_split_short_prefix():
    """Short provider prefix."""
    assert split_provider_and_model("o:gpt-4o") == ("o", "gpt-4o")


def test_split_with_suffix():
    """Provider:model:suffix keeps suffix attached to model."""
    assert split_provider_and_model("openai:o4-mini:high") == (
        "openai",
        "o4-mini:high",
    )


def test_split_anthropic_thinking():
    """Anthropic model with thinking token suffix."""
    assert split_provider_and_model(
        "anthropic:claude-opus-4-20250514:4k"
    ) == ("anthropic", "claude-opus-4-20250514:4k")


def test_split_invalid():
    """Missing colon raises ValueError."""
    with pytest.raises(ValueError):
        split_provider_and_model("nocolon")


def test_parse_thinking_k_notation():
    """k-notation suffix parsed to token count."""
    model, budget = parse_thinking_suffix("claude-opus-4-20250514:4k")
    assert model == "claude-opus-4-20250514"
    assert budget == 4096


def test_parse_thinking_1k():
    """1k suffix."""
    model, budget = parse_thinking_suffix("claude-sonnet-4-20250514:1k")
    assert model == "claude-sonnet-4-20250514"
    assert budget == 1024


def test_parse_thinking_exact():
    """Exact numeric suffix."""
    model, budget = parse_thinking_suffix("claude-opus-4-20250514:8000")
    assert model == "claude-opus-4-20250514"
    assert budget == 8000


def test_parse_thinking_effort():
    """OpenAI reasoning effort suffix returns string."""
    model, effort = parse_thinking_suffix("o4-mini:high")
    assert model == "o4-mini"
    assert effort == "high"


def test_parse_thinking_effort_low():
    """Low reasoning effort."""
    model, effort = parse_thinking_suffix("o3:low")
    assert model == "o3"
    assert effort == "low"


def test_parse_thinking_none():
    """No suffix returns None."""
    model, budget = parse_thinking_suffix("gpt-4o")
    assert model == "gpt-4o"
    assert budget is None


def test_parse_thinking_invalid_suffix():
    """Non-numeric, non-effort suffix returns None."""
    model, budget = parse_thinking_suffix("model:abc")
    assert model == "model:abc"
    assert budget is None
