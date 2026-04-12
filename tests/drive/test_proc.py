from unittest.mock import patch, MagicMock
from apps.drive.proc import list_claude_processes


@patch("apps.drive.proc.subprocess.run")
def test_list_processes(mock_run):
    mock_run.return_value = MagicMock(
        returncode=0,
        stdout="12345 claude -p some prompt\n67890 claude --init\n"
    )
    procs = list_claude_processes()
    assert len(procs) == 2
    assert procs[0]["pid"] == "12345"


@patch("apps.drive.proc.subprocess.run")
def test_no_processes(mock_run):
    mock_run.return_value = MagicMock(returncode=1, stdout="")
    procs = list_claude_processes()
    assert procs == []
