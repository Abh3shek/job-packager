from fastapi import FastAPI, HTTPException
from uuid import uuid4

from app.schemas import JobRequest, JobResponse
from app.packager import clone_repo, download_data, generate_scripts, create_tarball

app = FastAPI()

@app.post("/v1/jobs", response_model=JobResponse)
async def create_job(job: JobRequest):
    # Generating unique job id
    job_id = str(uuid4())

    # Clone the repo at specified commit
    try:
        clone_repo(job.git_url, job.commit_hash, job_id)
        download_data(job.data_url, job_id)
        generate_scripts(job.command, job_id)
        create_tarball(job_id)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Respond with a job id
    return JobResponse(job_id=job_id)

"""
sample schema
{
  "git_url": "https://github.com/octocat/Hello-World/",
  "commit_hash": "7fd1a60b01f91b314f59955a4e4d4e80d8edf11d",
  "data_url": "https://people.sc.fsu.edu/~jburkardt/data/csv/hw_200.csv",
  "command": "python main.py"
}
"""