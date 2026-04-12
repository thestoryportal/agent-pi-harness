from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from apps.direct.main import cli


@patch("apps.direct.main.httpx.Client")
@patch.dict("os.environ", {"LISTEN_API_KEY": "test-key", "LISTEN_PORT": "8420"})
def test_start_command(mock_client_cls):
    mock_client = MagicMock()
    mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
    mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)
    mock_client.post.return_value = MagicMock(
        status_code=201,
        json=MagicMock(return_value={"id": "abc123", "status": "pending"})
    )
    runner = CliRunner()
    result = runner.invoke(cli, ["start", "echo hello"])
    assert result.exit_code == 0
    assert "abc123" in result.output


@patch("apps.direct.main.httpx.Client")
@patch.dict("os.environ", {"LISTEN_API_KEY": "test-key", "LISTEN_PORT": "8420"})
def test_list_command(mock_client_cls):
    mock_client = MagicMock()
    mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
    mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)
    mock_client.get.return_value = MagicMock(
        status_code=200,
        json=MagicMock(return_value=[{"id": "a", "command": "c", "status": "pending"}])
    )
    runner = CliRunner()
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0


@patch("apps.direct.main.httpx.Client")
@patch.dict("os.environ", {"LISTEN_API_KEY": "test-key", "LISTEN_PORT": "8420"})
def test_get_command(mock_client_cls):
    mock_client = MagicMock()
    mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
    mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)
    mock_client.get.return_value = MagicMock(
        status_code=200,
        json=MagicMock(return_value={"id": "abc123", "status": "running", "command": "echo"})
    )
    runner = CliRunner()
    result = runner.invoke(cli, ["get", "abc123"])
    assert result.exit_code == 0
    assert "abc123" in result.output


@patch("apps.direct.main.httpx.Client")
@patch.dict("os.environ", {"LISTEN_API_KEY": "test-key", "LISTEN_PORT": "8420"})
def test_latest_command(mock_client_cls):
    mock_client = MagicMock()
    mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
    mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)
    mock_client.get.return_value = MagicMock(
        status_code=200,
        json=MagicMock(return_value=[{"id": "a", "command": "c", "status": "done"}])
    )
    runner = CliRunner()
    result = runner.invoke(cli, ["latest"])
    assert result.exit_code == 0


@patch("apps.direct.main.httpx.Client")
@patch.dict("os.environ", {"LISTEN_API_KEY": "test-key", "LISTEN_PORT": "8420"})
def test_stop_command(mock_client_cls):
    mock_client = MagicMock()
    mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
    mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)
    mock_client.delete.return_value = MagicMock(
        status_code=200,
        json=MagicMock(return_value={"deleted": "abc123"})
    )
    runner = CliRunner()
    result = runner.invoke(cli, ["stop", "abc123"])
    assert result.exit_code == 0
    assert "abc123" in result.output
