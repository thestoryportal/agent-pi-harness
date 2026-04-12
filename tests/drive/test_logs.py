from unittest.mock import patch, MagicMock
from apps.drive.logs import tail_logs


@patch("apps.drive.logs.subprocess.run")
def test_tail_logs(mock_run):
    mock_run.return_value = MagicMock(returncode=0, stdout="line1\nline2\n")
    output = tail_logs("agent-1", lines=10)
    assert "line1" in output


@patch("apps.drive.logs.subprocess.run")
def test_tail_logs_no_session(mock_run):
    mock_run.return_value = MagicMock(returncode=1, stdout="")
    output = tail_logs("nonexistent")
    assert output == ""
