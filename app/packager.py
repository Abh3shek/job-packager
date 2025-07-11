from git import Repo, GitCommandError, BadName, InvalidGitRepositoryError
import os
import requests
from urllib.parse import urlparse

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

        print(f"[SUCCESS] Checked out commit {commit_hash}")
    except (GitCommandError, BadName, InvalidGitRepositoryError, ValueError) as e:
        raise RuntimeError(f"Invalid Git URL or commit hash: {e}")

import os
import requests
from urllib.parse import urlparse

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
