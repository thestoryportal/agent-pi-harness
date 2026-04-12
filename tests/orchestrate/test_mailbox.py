"""Tests for apps.orchestrate.mailbox — agent-to-agent messaging."""

import pytest

from apps.orchestrate.mailbox import (
    broadcast,
    clear_mailboxes,
    drain_inbox,
    read_inbox,
    send_message,
)


def test_send_creates_inbox_file(tmp_path):
    mdir = tmp_path / "mailboxes"
    send_message("lead", "builder", "hello", mailbox_dir=mdir)
    assert (mdir / "builder.jsonl").exists()


def test_send_message_fields(tmp_path):
    mdir = tmp_path / "mailboxes"
    msg = send_message("lead", "builder", "hello", mailbox_dir=mdir)
    for key in ("message_id", "from_agent", "to_agent", "content", "type", "timestamp"):
        assert key in msg


def test_read_inbox_returns_messages(tmp_path):
    mdir = tmp_path / "mailboxes"
    send_message("lead", "builder", "a", mailbox_dir=mdir)
    send_message("lead", "builder", "b", mailbox_dir=mdir)
    send_message("lead", "builder", "c", mailbox_dir=mdir)
    msgs = read_inbox("builder", mailbox_dir=mdir)
    assert len(msgs) == 3


def test_read_inbox_empty_returns_empty(tmp_path):
    mdir = tmp_path / "mailboxes"
    assert read_inbox("builder", mailbox_dir=mdir) == []


def test_drain_clears_inbox(tmp_path):
    mdir = tmp_path / "mailboxes"
    send_message("lead", "builder", "a", mailbox_dir=mdir)
    send_message("lead", "builder", "b", mailbox_dir=mdir)
    msgs = drain_inbox("builder", mailbox_dir=mdir)
    assert len(msgs) == 2
    # Second read should be empty (agent messages drained)
    assert read_inbox("builder", mailbox_dir=mdir) == []


def test_drain_does_not_clear_broadcast(tmp_path):
    mdir = tmp_path / "mailboxes"
    broadcast("lead", "announcement", mailbox_dir=mdir)
    send_message("lead", "builder", "direct", mailbox_dir=mdir)
    drain_inbox("builder", mailbox_dir=mdir)
    # Broadcast should still be readable
    msgs = read_inbox("builder", mailbox_dir=mdir)
    assert len(msgs) == 1
    assert msgs[0]["to_agent"] == "*"


def test_broadcast_writes_to_broadcast_file(tmp_path):
    mdir = tmp_path / "mailboxes"
    broadcast("lead", "announcement", mailbox_dir=mdir)
    assert (mdir / "_broadcast.jsonl").exists()


def test_broadcast_visible_in_all_inboxes(tmp_path):
    mdir = tmp_path / "mailboxes"
    broadcast("lead", "announcement", mailbox_dir=mdir)
    builder_msgs = read_inbox("builder", mailbox_dir=mdir)
    validator_msgs = read_inbox("validator", mailbox_dir=mdir)
    assert len(builder_msgs) == 1
    assert len(validator_msgs) == 1
    assert builder_msgs[0]["content"] == "announcement"


def test_invalid_message_type_raises(tmp_path):
    mdir = tmp_path / "mailboxes"
    with pytest.raises(ValueError, match="invalid message_type"):
        send_message("lead", "builder", "hello", "unknown", mailbox_dir=mdir)


def test_clear_mailboxes(tmp_path):
    mdir = tmp_path / "mailboxes"
    send_message("lead", "builder", "a", mailbox_dir=mdir)
    broadcast("lead", "b", mailbox_dir=mdir)
    clear_mailboxes(mailbox_dir=mdir)
    assert list(mdir.glob("*.jsonl")) == []


def test_message_id_is_short_uuid(tmp_path):
    mdir = tmp_path / "mailboxes"
    msg = send_message("lead", "builder", "hello", mailbox_dir=mdir)
    assert len(msg["message_id"]) == 8
    assert msg["message_id"].isalnum()


def test_invalid_from_agent_raises(tmp_path):
    mdir = tmp_path / "mailboxes"
    with pytest.raises(ValueError, match="invalid agent name"):
        send_message("../../bad", "builder", "hello", mailbox_dir=mdir)


def test_invalid_to_agent_raises(tmp_path):
    mdir = tmp_path / "mailboxes"
    with pytest.raises(ValueError, match="invalid agent name"):
        send_message("lead", "../../bad", "hello", mailbox_dir=mdir)


def test_reserved_name_broadcast_raises(tmp_path):
    mdir = tmp_path / "mailboxes"
    with pytest.raises(ValueError, match="reserved"):
        send_message("lead", "_broadcast", "hello", mailbox_dir=mdir)


def test_broadcast_invalid_from_raises(tmp_path):
    mdir = tmp_path / "mailboxes"
    with pytest.raises(ValueError, match="invalid agent name"):
        broadcast("BAD AGENT", "hello", mailbox_dir=mdir)
