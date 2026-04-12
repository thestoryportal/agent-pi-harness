"""Sentinel token generation and parsing for tmux session completion detection.

Pattern from mac-mini-agent:
  echo "__START_<token>" ; <cmd> ; echo "__DONE_<token>:$?"

Poll watches for __DONE_<token>:<exit_code> in tmux output.
"""

import re
import secrets


def generate_token() -> str:
    """Generate a 12-char hex token for Sentinel wrapping."""
    return secrets.token_hex(6)


def wrap_command(cmd: str, token: str) -> str:
    """Wrap a command with Sentinel start/done markers."""
    return f'echo "__START_{token}" ; {cmd} ; echo "__DONE_{token}:$?"'


def parse_sentinel(output: str, token: str) -> int | None:
    """Parse tmux output for a Sentinel completion token.

    Returns exit code (int) if found, None if not yet completed.
    """
    pattern = rf"__DONE_{re.escape(token)}:(\d+)"
    match = re.search(pattern, output)
    if match:
        return int(match.group(1))
    return None
