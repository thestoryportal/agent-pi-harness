from apps.listen.models import Job, save_job, load_job, list_jobs


def test_job_creation():
    job = Job(command="uv sync", args=["--quiet"])
    assert job.status == "pending"
    assert job.id is not None
    assert len(job.id) == 8


def test_save_and_load_roundtrip(tmp_path):
    job = Job(command="echo hello")
    save_job(job, jobs_dir=tmp_path)
    loaded = load_job(job.id, jobs_dir=tmp_path)
    assert loaded.command == "echo hello"
    assert loaded.status == "pending"


def test_list_jobs(tmp_path):
    j1 = Job(command="cmd1")
    j2 = Job(command="cmd2")
    save_job(j1, jobs_dir=tmp_path)
    save_job(j2, jobs_dir=tmp_path)
    jobs = list_jobs(jobs_dir=tmp_path)
    assert len(jobs) == 2
