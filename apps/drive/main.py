"""Drive CLI — tmux session controller for ArhuGula.

Usage: uv run apps/drive/main.py <command> [options]
"""

import json
import click

from apps.drive.session import create_session, list_sessions, kill_session
from apps.drive.runner import run_command, send_text
from apps.drive.logs import tail_logs
from apps.drive.poll import poll_session
from apps.drive.fanout import dispatch_fanout, dispatch_fanout_from_file, DEFAULT_MAX_SESSIONS
from apps.drive.proc import list_claude_processes

# Token registry for poll — populated by run, consumed by poll
_active_tokens: dict[str, str] = {}  # session_name -> token


@click.group()
def cli():
    """Drive — tmux session controller."""
    pass


@cli.group()
def session():
    """Manage tmux sessions."""
    pass


@session.command("create")
@click.option("--name", required=True, help="Session name")
def session_create(name):
    if create_session(name):
        click.echo(f"Created session: {name}")
    else:
        click.echo(f"Failed to create session: {name}", err=True)
        raise SystemExit(1)


@session.command("list")
def session_list():
    for name in list_sessions():
        click.echo(name)


@session.command("kill")
@click.option("--name", required=True, help="Session name")
def session_kill(name):
    if kill_session(name):
        click.echo(f"Killed session: {name}")
    else:
        click.echo(f"Failed to kill session: {name}", err=True)
        raise SystemExit(1)


@cli.command()
@click.option("--session", "session_name", required=True, help="Target session")
@click.argument("cmd")
def run(session_name, cmd):
    """Execute a command with Sentinel wrapping."""
    token = run_command(session_name, cmd)
    if token:
        _active_tokens[session_name] = token
        click.echo(json.dumps({"session": session_name, "token": token, "status": "dispatched"}))
    else:
        click.echo("Failed to dispatch command", err=True)
        raise SystemExit(1)


@cli.command()
@click.option("--session", "session_name", required=True, help="Target session")
@click.argument("text")
def send(session_name, text):
    """Send raw text to a session (no Sentinel)."""
    if send_text(session_name, text):
        click.echo("Sent")
    else:
        click.echo("Failed", err=True)
        raise SystemExit(1)


@cli.command()
@click.option("--session", "session_name", required=True, help="Target session")
@click.option("--lines", default=50, help="Number of lines")
def logs(session_name, lines):
    """Tail session output."""
    click.echo(tail_logs(session_name, lines))


@cli.command()
def poll():
    """Poll all sessions with active tokens for Sentinel completion."""
    if not _active_tokens:
        click.echo("No active tokens. Use 'run' to dispatch commands first.")
        return
    for session_name, token in list(_active_tokens.items()):
        result = poll_session(session_name, token)
        if result is not None:
            click.echo(f"  {session_name}: DONE (exit={result})")
            del _active_tokens[session_name]
        else:
            click.echo(f"  {session_name}: RUNNING (token={token})")


@cli.command()
@click.argument("cmd", required=False, default="")
@click.option("--targets", default="", help="Comma-separated session names")
@click.option("--max-sessions", default=DEFAULT_MAX_SESSIONS, help="Max parallel sessions")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.option("--file", "from_file", type=click.Path(exists=True), help="Read commands from file (one per line)")
def fanout(cmd, targets, max_sessions, as_json, from_file):
    """Dispatch command to multiple sessions in parallel."""
    if from_file:
        results = dispatch_fanout_from_file(from_file, max_sessions=max_sessions)
    elif cmd and targets:
        target_list = [t.strip() for t in targets.split(",")]
        results = dispatch_fanout(cmd, targets=target_list, max_sessions=max_sessions)
    else:
        click.echo("Provide --file or (cmd + --targets)", err=True)
        raise SystemExit(1)

    if as_json:
        click.echo(json.dumps(results, indent=2))
    else:
        for target, info in results.items():
            status = info.get("status", "unknown")
            token = info.get("token", "none")
            click.echo(f"  {target}: {status} (token={token})")


@cli.command()
def proc():
    """List running Claude Code processes."""
    processes = list_claude_processes()
    if not processes:
        click.echo("No Claude Code processes running")
    else:
        for p in processes:
            click.echo(f"  PID {p['pid']}: {p['command']}")


if __name__ == "__main__":
    cli()
