"""Tests for prompt_from_file molecule."""

import pytest
from unittest.mock import patch

from just_prompt.molecules.prompt_from_file import (
    prompt_from_file,
    prompt_from_file_to_file,
)


@pytest.fixture(autouse=True)
def _allow_tmp_path(tmp_path, monkeypatch):
    """Allow tmp_path as the root for path validation in all tests."""
    monkeypatch.setenv("JUST_PROMPT_ALLOWED_ROOT", str(tmp_path))


@patch("just_prompt.molecules.prompt_from_file.prompt_fn")
def test_prompt_from_file_reads_and_dispatches(mock_prompt_fn, tmp_path):
    """Reads file content and dispatches to prompt."""
    prompt_file = tmp_path / "test_prompt.txt"
    prompt_file.write_text("test prompt text")
    mock_prompt_fn.return_value = {"openai:gpt-4o": "response"}

    result = prompt_from_file(
        str(prompt_file), ["openai:gpt-4o"]
    )
    assert result == {"openai:gpt-4o": "response"}
    mock_prompt_fn.assert_called_once_with(
        "test prompt text", ["openai:gpt-4o"]
    )


def test_prompt_from_file_relative_path_raises():
    """Relative path raises ValueError."""
    with pytest.raises(ValueError, match="must be absolute"):
        prompt_from_file("./relative/path.txt")


def test_prompt_from_file_missing_raises(tmp_path):
    """Missing file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        prompt_from_file(str(tmp_path / "nonexistent.txt"))


@patch("just_prompt.molecules.prompt_from_file.prompt_fn")
def test_prompt_from_file_to_file_relative_output_raises(
    mock_prompt_fn, tmp_path
):
    """Relative output dir raises ValueError."""
    prompt_file = tmp_path / "prompt.txt"
    prompt_file.write_text("test")
    mock_prompt_fn.return_value = {"openai:gpt-4o": "response"}

    with pytest.raises(ValueError, match="must be absolute"):
        prompt_from_file_to_file(
            str(prompt_file), ["openai:gpt-4o"], "./relative"
        )


@patch("just_prompt.molecules.prompt_from_file.prompt_fn")
def test_prompt_from_file_to_file_saves(mock_prompt_fn, tmp_path):
    """Saves each model response as a markdown file."""
    prompt_file = tmp_path / "prompt.txt"
    prompt_file.write_text("test")
    output_dir = tmp_path / "output"

    mock_prompt_fn.return_value = {
        "openai:gpt-4o": "GPT response",
        "anthropic:claude-sonnet-4-20250514": "Claude response",
    }

    result = prompt_from_file_to_file(
        str(prompt_file),
        ["openai:gpt-4o", "anthropic:claude-sonnet-4-20250514"],
        str(output_dir),
    )

    assert len(result) == 2
    assert (output_dir / "openai_gpt-4o_response.md").exists()
    assert (
        output_dir / "openai_gpt-4o_response.md"
    ).read_text() == "GPT response"
