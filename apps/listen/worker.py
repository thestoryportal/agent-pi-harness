"""Job worker — spawns Claude Code agents as subprocesses via Drive."""

import subprocess
import threading
from datetime import datetime, timezone
from pathlib import Path

from apps.listen.models import Job, save_job


def run_job(job: Job, jobs_dir: Path) -> None:
    """Execute a job by dispatching to Drive in a background thread."""
    job.status = "running"
    job.started_at = datetime.now(timezone.utc).isoformat()
    job.session_name = f"job-{job.id}"
    save_job(job, jobs_dir=jobs_dir)

    def _worker():
        try:
            result = subprocess.run(
                ["uv", "run", "apps/drive/main.py", "run",
                 "--session", job.session_name, job.command],
                capture_output=True, text=True, timeout=3600,
            )
            job.exit_code = result.returncode
            job.status = "completed" if result.returncode == 0 else "failed"
        except subprocess.TimeoutExpired:
            job.status = "timeout"
        except Exception as e:
            job.status = f"error: {e}"
        finally:
            job.completed_at = datetime.now(timezone.utc).isoformat()
            save_job(job, jobs_dir=jobs_dir)

    thread = threading.Thread(target=_worker, daemon=True)
    thread.start()
