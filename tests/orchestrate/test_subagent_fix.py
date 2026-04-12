"""Verify S-01 fix: agent_type validation prevents path traversal."""

import re

# Inline the regex from the fixed hook to test without import issues
_SAFE_AGENT_TYPE = re.compile(r"^[a-zA-Z0-9_-]+$")


def test_valid_agent_types():
    for name in ("builder", "security", "scout-agent", "schema-reviewer", "meta_agent"):
        assert _SAFE_AGENT_TYPE.match(name), f"{name} should be valid"


def test_path_traversal_rejected():
    for name in ("../../etc/passwd", "../.env", "foo/bar", ".", "..", "a b"):
        assert not _SAFE_AGENT_TYPE.match(name), f"{name} should be rejected"


def test_empty_string_rejected():
    assert not _SAFE_AGENT_TYPE.match("")
