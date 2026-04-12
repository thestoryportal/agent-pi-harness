from unittest.mock import patch, MagicMock
from apps.drive.runner import run_command, send_text


@patch("apps.drive.runner.subprocess.run")
def test_run_command_sends_wrapped(mock_run):
    mock_run.return_value = MagicMock(returncode=0)
    token = run_command("agent-1", "uv sync")
    assert token is not None
    assert len(token) == 12
    cmd = mock_run.call_args[0][0]
    cmd_str = " ".join(cmd)
    assert "send-keys" in cmd_str
    assert "__START_" in cmd_str
    assert "__DONE_" in cmd_str


@patch("apps.drive.runner.subprocess.run")
def test_send_text_no_sentinel(mock_run):
    mock_run.return_value = MagicMock(returncode=0)
    result = send_text("agent-1", "hello world")
    assert result is True
    cmd = mock_run.call_args[0][0]
    cmd_str = " ".join(cmd)
    assert "send-keys" in cmd_str
    assert "__DONE_" not in cmd_str
