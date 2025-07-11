from git import Repo, GitCommandError, BadName, InvalidGitRepositoryError
import os
import requests
from urllib.parse import urlparse
import tarfile
import shutil

def clone_repo(git_url: str, commit_hash: str, job_id: str):
    job_path = os.path.join("jobs", job_id)
    code_path = os.path.join(job_path, "code")
    os.makedirs(code_path, exist_ok=True)

    try:
        print(f"[INFO] Cloning {git_url} into {code_path}")
        repo = Repo.clone_from(git_url, code_path)

        # Try to resolve the commit
        commit = repo.commit(commit_hash)
        repo.git.checkout(commit)

        git_dir = os.path.join(code_path, ".git")
        if os.path.exists(git_dir):
            shutil.rmtree(git_dir)

        print(f"[SUCCESS] Checked out commit {commit_hash}")
    except (GitCommandError, BadName, InvalidGitRepositoryError, ValueError) as e:
        raise RuntimeError(f"Invalid Git URL or commit hash: {e}")

def download_data(data_url: str, job_id: str) -> None:
    try:
        print(f"[INFO] Downloading data from: {data_url}")
        response = requests.get(str(data_url), timeout=10)
        response.raise_for_status()

        # Extract filename from URL
        parsed = urlparse(str(data_url))
        filename = os.path.basename(parsed.path)
        if not filename:
            raise RuntimeError("Invalid data URL — no filename found.")

        data_path = os.path.join("jobs", job_id, "data")
        os.makedirs(data_path, exist_ok=True)

        file_path = os.path.join(data_path, filename)

        with open(file_path, "wb") as f:
            f.write(response.content)

        print(f"[SUCCESS] Data saved to: {file_path}")

    except requests.RequestException as e:
        raise RuntimeError(f"Failed to download data file: {e}")

def generate_scripts(command: str, job_id: str) -> None:
    # Generates run.sh and docker file inside jobs/{job_id}/
    job_path = os.path.join("jobs", job_id)

    try:
        run_sh_content = f"""#!/bin/bash
cd /code
{command}"""
        run_sh_path = os.path.join(job_path, "run.sh")
        with open(run_sh_path, "w") as f:
            f.write(run_sh_content)
        os.chmod(run_sh_path, 0o7555) # for making it executable

        # ===== Write a dockerfile ======
        dockerfile_content = f"""FROM python:3.10-slim

WORKDIR /app
COPY code/ /code
COPY data/ /data
COPY run.sh/ /run.sh

RUN chmod +x /run.sh

CMD ["sh", "/run.sh"]"""
        dockerfile_path = os.path.join(job_path, "Dockerfile")
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile_content)

        print(f"[SUCCESS] Generated run.sh and Dockerfile in {job_path}")
    except Exception as e:
        raise RuntimeError(f"Failed to generate build scripts: {e}")
    
def create_tarball(job_id: str) -> str:
    job_path = os.path.join("jobs", job_id)
    tar_path = os.path.join("jobs", f"{job_id}.tar.gz")

    try:
        with tarfile.open(tar_path, "w|gz") as tar:
            tar.add(job_path, arcname=job_id)
        print(f"[SUCCESS] Created tarball: {tar_path}")
        return tar_path
    except Exception as e:
        raise RuntimeError(f"Failed to create tarball: {e}")