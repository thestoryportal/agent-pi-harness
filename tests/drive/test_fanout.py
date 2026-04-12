from unittest.mock import patch
from apps.drive.fanout import dispatch_fanout, DEFAULT_MAX_SESSIONS


def test_default_cap():
    assert DEFAULT_MAX_SESSIONS == 2


@patch("apps.drive.fanout.run_command")
@patch("apps.drive.fanout.create_session")
def test_fanout_single_target(mock_create, mock_run):
    mock_create.return_value = True
    mock_run.return_value = "abc123"
    results = dispatch_fanout("uv sync", targets=["agent-1"])
    assert len(results) == 1
    assert results["agent-1"]["token"] == "abc123"


@patch("apps.drive.fanout.run_command")
@patch("apps.drive.fanout.create_session")
def test_fanout_respects_cap(mock_create, mock_run):
    mock_create.return_value = True
    mock_run.return_value = "abc123"
    targets = [f"agent-{i}" for i in range(5)]
    results = dispatch_fanout("echo hi", targets=targets, max_sessions=2)
    assert len(results) == 5  # all dispatched, but only 2 at a time
