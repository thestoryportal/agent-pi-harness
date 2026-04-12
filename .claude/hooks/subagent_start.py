#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""SubagentStart hook: log subagent initialization with tool isolation info.

Reads agent frontmatter from .claude/agents/{agent_type}.md to extract
declared tools and disallowedTools. Informational logging only — enforcement
is handled by agent frontmatter (O07) and PreToolUse hooks (SP2).
"""

import os
import re
import sys
from pathlib import Path

PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
sys.path.insert(0, str(Path(PROJECT_DIR) / ".claude" / "hooks"))
try:
    from _base import Logger, emit_event, handle_health_check, read_stdin, run_hook
except Exception:
    sys.exit(2)

HOOK_NAME = "subagent_start.py"
handle_health_check(HOOK_NAME)

AGENTS_DIR = Path(PROJECT_DIR) / ".claude" / "agents"
_SAFE_AGENT_TYPE = re.compile(r"^[a-zA-Z0-9_-]+$")


def _parse_frontmatter(filepath: Path) -> dict:
    """Parse YAML frontmatter from an agent .md file."""
    try:
        text = filepath.read_text()
    except OSError:
        return {}

    if not text.startswith("---"):
        return {}

    end = text.find("---", 3)
    if end == -1:
        return {}

    yaml_block = text[3:end].strip()
    try:
        import yaml
        return yaml.safe_load(yaml_block) or {}
    except Exception:
        return {}


def main():
    import time
    logger = Logger("subagent_start")
    start_time = time.monotonic()

    d = read_stdin()
    agent_id = d.get("agent_id", "unknown")
    agent_type = d.get("agent_type", "unknown")

    # Validate agent_type to prevent path traversal (S-01)
    tools = None
    disallowed_tools = None

    if not _SAFE_AGENT_TYPE.match(agent_type):
        logger.log(
            f"SubagentStart: {agent_id} ({agent_type}) "
            f"| REJECTED: invalid agent_type (path traversal risk)"
        )
    else:
        agent_file = AGENTS_DIR / f"{agent_type}.md"

        if agent_file.exists():
            fm = _parse_frontmatter(agent_file)
            tools = fm.get("tools")
            disallowed_tools = fm.get("disallowedTools")
            logger.log(
                f"SubagentStart: {agent_id} ({agent_type}) "
                f"| allowed={tools} | disallowed={disallowed_tools}"
            )
        else:
            logger.log(
                f"SubagentStart: {agent_id} ({agent_type}) "
                f"| WARNING: no agent definition for {agent_type}"
            )

    payload = {
        "agent_id": agent_id,
        "agent_type": agent_type,
        "tools": tools,
        "disallowed_tools": disallowed_tools,
    }

    elapsed = int((time.monotonic() - start_time) * 1000)
    emit_event("SubagentStart", HOOK_NAME, 0, payload, elapsed)
    sys.exit(0)

if __name__ == "__main__":
    run_hook(main, HOOK_NAME, event_type="SubagentStart")
