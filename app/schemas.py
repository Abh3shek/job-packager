from pydantic import BaseModel, HttpUrl, constr

class JobRequest(BaseModel):
    git_url: HttpUrl
    commit_hash: constr(min_length=7, max_length=40, pattern=r"^[a-fA-F0-9]+$")
    data_url: HttpUrl
    command: str

class JobResponse(BaseModel):
    job_id: str