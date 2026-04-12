"""Listen — FastAPI job server for ArhuGula.

Usage: uv run apps/listen/main.py
"""

import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from apps.listen.auth import require_api_key
from apps.listen.models import Job, save_job, load_job, list_jobs
from apps.listen.worker import run_job


def create_app(jobs_dir: str | Path | None = None) -> FastAPI:
    """Create the FastAPI app. jobs_dir is configurable for testing."""
    app = FastAPI(title="ArhuGula Listen", version="0.1.0")
    app.middleware("http")(require_api_key)

    _jobs_dir = Path(jobs_dir) if jobs_dir else Path("apps/listen/jobs")

    @app.post("/job", status_code=201)
    async def create_job(request: Request):
        body = await request.json()
        job = Job(
            command=body.get("command", ""),
            args=body.get("args", []),
        )
        save_job(job, jobs_dir=_jobs_dir)
        run_job(job, jobs_dir=_jobs_dir)
        return {"id": job.id, "status": job.status, "command": job.command}

    @app.get("/job/{job_id}")
    async def get_job(job_id: str):
        job = load_job(job_id, jobs_dir=_jobs_dir)
        if not job:
            return JSONResponse(status_code=404, content={"error": "Job not found"})
        return {
            "id": job.id, "command": job.command, "status": job.status,
            "created_at": job.created_at, "started_at": job.started_at,
            "completed_at": job.completed_at, "exit_code": job.exit_code,
        }

    @app.get("/jobs")
    async def get_jobs():
        return [
            {"id": j.id, "command": j.command, "status": j.status}
            for j in list_jobs(jobs_dir=_jobs_dir)
        ]

    @app.delete("/job/{job_id}")
    async def delete_job(job_id: str):
        path = _jobs_dir / f"{job_id}.yaml"
        if not path.exists():
            return JSONResponse(status_code=404, content={"error": "Job not found"})
        path.unlink()
        return {"deleted": job_id}

    return app


if __name__ == "__main__":
    port = int(os.environ.get("LISTEN_PORT", "8420"))
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=port)
