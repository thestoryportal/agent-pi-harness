"""Job data model with YAML persistence."""

import secrets
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path

import yaml


@dataclass
class Job:
    command: str
    args: list[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: secrets.token_hex(4))
    status: str = "pending"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    started_at: str | None = None
    completed_at: str | None = None
    exit_code: int | None = None
    session_name: str | None = None


def save_job(job: Job, jobs_dir: Path = Path("apps/listen/jobs")) -> None:
    """Save job state to YAML file."""
    jobs_dir.mkdir(parents=True, exist_ok=True)
    path = jobs_dir / f"{job.id}.yaml"
    with open(path, "w") as f:
        yaml.dump(asdict(job), f, default_flow_style=False)


def load_job(job_id: str, jobs_dir: Path = Path("apps/listen/jobs")) -> Job | None:
    """Load job state from YAML file."""
    path = jobs_dir / f"{job_id}.yaml"
    if not path.exists():
        return None
    with open(path) as f:
        data = yaml.safe_load(f)
    return Job(**data)


def list_jobs(jobs_dir: Path = Path("apps/listen/jobs")) -> list[Job]:
    """List all jobs from YAML files."""
    jobs_dir.mkdir(parents=True, exist_ok=True)
    jobs = []
    for path in sorted(jobs_dir.glob("*.yaml")):
        with open(path) as f:
            data = yaml.safe_load(f)
        jobs.append(Job(**data))
    return jobs
