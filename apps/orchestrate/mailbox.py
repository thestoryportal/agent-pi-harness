"""Mailbox communication — agent-to-agent message + broadcast primitives.

Per-agent JSONL inboxes with file locking. Follows update_log.py patterns.
Message types: task, status, alert, query.
"""

import fcntl
import json
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

MAILBOX_DIR = (
    Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))
    / "apps"
    / "orchestrate"
    / "logs"
    / "mailboxes"
)
MESSAGE_TYPES = ("task", "status", "alert", "query")
BROADCAST_FILE = "_broadcast.jsonl"
_SAFE_NAME = re.compile(r"[a-z0-9_-]+")


_RESERVED_NAMES = frozenset({"_broadcast"})


def _validate_agent_name(agent: str) -> None:
    """Reject agent names that could cause path traversal or namespace collision."""
    if not _SAFE_NAME.fullmatch(agent):
        raise ValueError(
            f"invalid agent name {agent!r}: must match [a-z0-9_-]+"
        )
    if agent in _RESERVED_NAMES:
        raise ValueError(f"agent name {agent!r} is reserved")


def _inbox_path(agent: str, mailbox_dir: Path) -> Path:
    _validate_agent_name(agent)
    return mailbox_dir / f"{agent}.jsonl"


def _broadcast_path(mailbox_dir: Path) -> Path:
    return mailbox_dir / BROADCAST_FILE


def _append_message(path: Path, message: dict) -> None:
    """Append a single message to a JSONL file under exclusive lock."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            f.write(json.dumps(message) + "\n")
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def _read_jsonl(path: Path) -> list[dict]:
    """Read all messages from a JSONL file. Skips malformed lines."""
    if not path.exists():
        return []
    messages: list[dict] = []
    with open(path) as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_SH)
        try:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    messages.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    return messages


def _drain_file(path: Path) -> list[dict]:
    """Read and clear a JSONL file under a single exclusive lock.

    Truncates the file to zero bytes rather than unlinking, so the lock
    is held for the full read-clear cycle with no TOCTOU gap.
    """
    if not path.exists():
        return []
    messages: list[dict] = []
    with open(path, "r+") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    messages.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
            f.seek(0)
            f.truncate()
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    return messages


def _make_message(
    from_agent: str,
    to_agent: str,
    content: str,
    message_type: str,
) -> dict:
    if message_type not in MESSAGE_TYPES:
        raise ValueError(
            f"invalid message_type {message_type!r}, must be one of {MESSAGE_TYPES}"
        )
    return {
        "message_id": uuid.uuid4().hex[:8],
        "from_agent": from_agent,
        "to_agent": to_agent,
        "content": content,
        "type": message_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def send_message(
    from_agent: str,
    to_agent: str,
    content: str,
    message_type: str = "status",
    *,
    mailbox_dir: Path | None = None,
) -> dict:
    """Send a 1:1 message to to_agent's inbox.

    Raises ValueError if message_type not in MESSAGE_TYPES or agent names invalid.
    """
    _validate_agent_name(from_agent)
    mdir = mailbox_dir or MAILBOX_DIR
    message = _make_message(from_agent, to_agent, content, message_type)
    _append_message(_inbox_path(to_agent, mdir), message)
    return message


def broadcast(
    from_agent: str,
    content: str,
    message_type: str = "status",
    *,
    mailbox_dir: Path | None = None,
) -> dict:
    """Broadcast to all agents (to_agent='*'). Writes to _broadcast.jsonl."""
    _validate_agent_name(from_agent)
    mdir = mailbox_dir or MAILBOX_DIR
    message = _make_message(from_agent, "*", content, message_type)
    _append_message(_broadcast_path(mdir), message)
    return message


def read_inbox(
    agent: str,
    drain: bool = False,
    *,
    mailbox_dir: Path | None = None,
) -> list[dict]:
    """Read messages from agent's inbox + broadcast messages.

    If drain=True, read and clear the agent's inbox atomically.
    Broadcast messages are never drained by individual agent reads.
    """
    mdir = mailbox_dir or MAILBOX_DIR
    inbox = _inbox_path(agent, mdir)

    if drain:
        agent_messages = _drain_file(inbox)
    else:
        agent_messages = _read_jsonl(inbox)

    broadcast_messages = _read_jsonl(_broadcast_path(mdir))
    return agent_messages + broadcast_messages


def drain_inbox(
    agent: str,
    *,
    mailbox_dir: Path | None = None,
) -> list[dict]:
    """Read and clear agent's inbox. Broadcast messages remain."""
    return read_inbox(agent, drain=True, mailbox_dir=mailbox_dir)


def clear_mailboxes(*, mailbox_dir: Path | None = None) -> None:
    """Delete all JSONL inbox files under mailbox_dir. For testing only."""
    mdir = mailbox_dir or MAILBOX_DIR
    if mdir.exists():
        for f in mdir.glob("*.jsonl"):
            f.unlink()
