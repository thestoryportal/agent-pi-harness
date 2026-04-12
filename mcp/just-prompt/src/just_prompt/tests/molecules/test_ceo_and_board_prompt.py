"""Tests for ceo_and_board molecule."""

import pytest
from unittest.mock import patch

from just_prompt.molecules.ceo_and_board_prompt import (
    _wrap_board_response,
    ceo_and_board,
)


@pytest.fixture(autouse=True)
def _allow_tmp_path(tmp_path, monkeypatch):
    """Allow tmp_path as the root for path validation in all tests."""
    monkeypatch.setenv("JUST_PROMPT_ALLOWED_ROOT", str(tmp_path))


def test_wrap_board_response():
    """XML envelope wraps model and response correctly."""
    result = _wrap_board_response("openai:gpt-4o", "test response")
    assert result.startswith('<board_member_response model="openai:gpt-4o">')
    assert "test response" in result
    assert result.endswith("</board_member_response>")


@patch("just_prompt.molecules.ceo_and_board_prompt.ModelRouter")
def test_ceo_and_board_full_flow(mock_router, tmp_path):
    """Full flow: fan-out, collection, CEO synthesis."""
    prompt_file = tmp_path / "prompt.txt"
    prompt_file.write_text("What should we build?")
    output_dir = tmp_path / "output"

    call_count = 0

    def side_effect(model, text):
        nonlocal call_count
        call_count += 1
        if "board_member_response" in text or "CEO" in text:
            return "CEO final decision"
        return f"Board response from {model}"

    mock_router.route_prompt.side_effect = side_effect

    result = ceo_and_board(
        abs_file_path=str(prompt_file),
        models_prefixed_by_provider=["openai:gpt-4o", "anthropic:claude-sonnet-4-20250514"],
        abs_output_dir=str(output_dir),
        ceo_model="openai:o3",
    )

    assert result == "CEO final decision"
    assert (output_dir / "ceo_decision.md").exists()
    assert (output_dir / "openai_gpt-4o_response.md").exists()
    assert (
        output_dir / "anthropic_claude-sonnet-4-20250514_response.md"
    ).exists()
    # 2 board members + 1 CEO = 3 route_prompt calls
    assert mock_router.route_prompt.call_count == 3


def test_ceo_and_board_path_traversal_blocked(tmp_path):
    """Path outside allowed root raises ValueError."""
    with pytest.raises(ValueError, match="must be within"):
        ceo_and_board(abs_file_path="/etc/passwd")


def test_ceo_and_board_output_traversal_blocked(tmp_path):
    """Output dir outside allowed root raises ValueError."""
    prompt_file = tmp_path / "prompt.txt"
    prompt_file.write_text("test")
    with pytest.raises(ValueError, match="must be within"):
        ceo_and_board(
            abs_file_path=str(prompt_file),
            abs_output_dir="/tmp",
        )


def test_ceo_and_board_relative_path_raises():
    """Relative input path raises ValueError."""
    with pytest.raises(ValueError, match="must be absolute"):
        ceo_and_board(abs_file_path="./relative.txt")


def test_ceo_and_board_missing_file_raises(tmp_path):
    """Missing file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        ceo_and_board(
            abs_file_path=str(tmp_path / "nonexistent.txt"),
            abs_output_dir=str(tmp_path),
        )


def test_ceo_and_board_relative_output_raises(tmp_path):
    """Relative output dir raises ValueError."""
    prompt_file = tmp_path / "prompt.txt"
    prompt_file.write_text("test")
    with pytest.raises(ValueError, match="must be absolute"):
        ceo_and_board(
            abs_file_path=str(prompt_file),
            abs_output_dir="./relative",
        )


@patch("just_prompt.molecules.ceo_and_board_prompt.ModelRouter")
def test_ceo_and_board_error_captured(mock_router, tmp_path):
    """Board member error is captured, CEO still runs."""
    prompt_file = tmp_path / "prompt.txt"
    prompt_file.write_text("test")
    output_dir = tmp_path / "output"

    call_count = 0

    def side_effect(model, text):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise RuntimeError("API down")
        return "response"

    mock_router.route_prompt.side_effect = side_effect

    result = ceo_and_board(
        abs_file_path=str(prompt_file),
        models_prefixed_by_provider=["openai:gpt-4o"],
        abs_output_dir=str(output_dir),
        ceo_model="openai:o3",
    )

    assert result == "response"
    # Board error captured in file
    error_file = output_dir / "openai_gpt-4o_response.md"
    assert error_file.exists()
    assert "ERROR:" in error_file.read_text()
