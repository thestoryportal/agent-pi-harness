"""Tests for MCP server creation."""

from just_prompt.server import create_server


def test_server_creates():
    """Server can be created without error."""
    server = create_server(["anthropic:claude-sonnet-4-20250514"])
    assert server is not None
    assert server.name == "just-prompt"
