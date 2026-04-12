from unittest.mock import patch, MagicMock
from apps.drive.poll import capture_pane, poll_session


@patch("apps.drive.poll.subprocess.run")
def test_capture_pane(mock_run):
    mock_run.return_value = MagicMock(
        returncode=0,
        stdout="line1\nline2\n__DONE_abc123:0\nline3\n"
    )
    output = capture_pane("agent-1")
    assert "__DONE_abc123:0" in output


@patch("apps.drive.poll.capture_pane")
def test_poll_session_completed(mock_capture):
    mock_capture.return_value = "output\n__DONE_abc123:0\n"
    result = poll_session("agent-1", "abc123")
    assert result == 0


@patch("apps.drive.poll.capture_pane")
def test_poll_session_pending(mock_capture):
    mock_capture.return_value = "still running...\n"
    result = poll_session("agent-1", "abc123")
    assert result is None
