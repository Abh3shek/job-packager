from fastapi import FastAPI, HTTPException
from uuid import uuid4

from app.schemas import JobRequest, JobResponse
from app.packager import clone_repo, download_data

app = FastAPI()

@app.post("/v1/jobs", response_model=JobResponse)
async def create_job(job: JobRequest):
    # Generating unique job id
    job_id = str(uuid4())

    # Clone the repo at specified commit
    try:
        clone_repo(job.git_url, job.commit_hash, job_id)
        download_data(job.data_url, job_id)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Respond with a job id
    return JobResponse(job_id=job_id)