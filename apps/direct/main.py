"""Direct — CLI client for ArhuGula Listen server.

Usage: uv run apps/direct/main.py <command> [options]
"""

import json
import os

import click
import httpx


def get_base_url() -> str:
    port = os.environ.get("LISTEN_PORT", "8420")
    return f"http://127.0.0.1:{port}"


def get_headers() -> dict:
    key = os.environ.get("LISTEN_API_KEY", "")
    return {"X-API-Key": key} if key else {}


@click.group()
def cli():
    """Direct — CLI client for Listen job server."""
    pass


@cli.command()
@click.argument("command")
@click.option("--args", "cmd_args", default="", help="Comma-separated args")
def start(command, cmd_args):
    """Submit a new job to Listen."""
    args_list = [a.strip() for a in cmd_args.split(",") if a.strip()] if cmd_args else []
    with httpx.Client() as client:
        response = client.post(
            f"{get_base_url()}/job",
            json={"command": command, "args": args_list},
            headers=get_headers(),
        )
    data = response.json()
    click.echo(json.dumps(data, indent=2))


@cli.command()
@click.argument("job_id")
def get(job_id):
    """Get job status by ID."""
    with httpx.Client() as client:
        response = client.get(f"{get_base_url()}/job/{job_id}", headers=get_headers())
    click.echo(json.dumps(response.json(), indent=2))


@cli.command("list")
def list_jobs():
    """List all jobs."""
    with httpx.Client() as client:
        response = client.get(f"{get_base_url()}/jobs", headers=get_headers())
    jobs = response.json()
    if not jobs:
        click.echo("No jobs")
    else:
        for j in jobs:
            click.echo(f"  {j['id']}  {j['status']:10s}  {j['command']}")


@cli.command()
def latest():
    """Get the most recent job."""
    with httpx.Client() as client:
        response = client.get(f"{get_base_url()}/jobs", headers=get_headers())
    jobs = response.json()
    if not jobs:
        click.echo("No jobs")
    else:
        click.echo(json.dumps(jobs[-1], indent=2))


@cli.command()
@click.argument("job_id")
def stop(job_id):
    """Cancel a job by ID."""
    with httpx.Client() as client:
        response = client.delete(f"{get_base_url()}/job/{job_id}", headers=get_headers())
    click.echo(json.dumps(response.json(), indent=2))


@cli.command("jobs")
def jobs_alias():
    """Alias for 'list'."""
    list_jobs.invoke(click.Context(list_jobs))


if __name__ == "__main__":
    cli()
