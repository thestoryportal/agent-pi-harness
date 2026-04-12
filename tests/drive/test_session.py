from unittest.mock import patch, MagicMock
from apps.drive.session import create_session, list_sessions, kill_session


@patch("apps.drive.session.subprocess.run")
def test_create_session(mock_run):
    mock_run.return_value = MagicMock(returncode=0)
    result = create_session("agent-1")
    mock_run.assert_called_once()
    cmd = mock_run.call_args[0][0]
    assert "tmux" in cmd
    assert "new-session" in cmd
    assert "agent-1" in cmd
    assert result is True


@patch("apps.drive.session.subprocess.run")
def test_list_sessions(mock_run):
    mock_run.return_value = MagicMock(
        returncode=0,
        stdout="agent-1\nagent-2\n"
    )
    sessions = list_sessions()
    assert sessions == ["agent-1", "agent-2"]


@patch("apps.drive.session.subprocess.run")
def test_list_sessions_none(mock_run):
    mock_run.return_value = MagicMock(returncode=1, stdout="")
    sessions = list_sessions()
    assert sessions == []


@patch("apps.drive.session.subprocess.run")
def test_kill_session(mock_run):
    mock_run.return_value = MagicMock(returncode=0)
    result = kill_session("agent-1")
    cmd = mock_run.call_args[0][0]
    assert "kill-session" in cmd
    assert result is True
