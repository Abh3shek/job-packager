# 🧩 Asynchronous Job Execution Packager

A powerful microservice to **automatically bundle user-submitted code, data, and execution commands** into a portable `.tar.gz` archive — ready for Dockerized, reproducible job execution. ⚙️📦

---

## 🚀 Features at a Glance

✨ Everything you need to prep jobs in one go:

- 🔁 Clone any public Git repository at a specific commit
- 📥 Download external datasets via URL
- ⚙️ Auto-generate a `run.sh` script and a `Dockerfile`
- 📦 Create a compressed, container-ready `.tar.gz` archive
- 🧼 Clean and modular FastAPI backend for robust API support

---

## 🌐 API Overview

### 📬 Endpoint: `POST /v1/jobs`

Send a job specification and receive a **packaged** artifact ID.

#### 📝 Request Example:

```json
{
  "git_url": "https://github.com/octocat/Hello-World",
  "commit_hash": "7fd1a60b01f91b314f59955a4e4d4e80d8edf11d",
  "data_url": "https://people.sc.fsu.edu/~jburkardt/data/csv/hw_200.csv",
  "command": "python main.py"
}
```

#### 📦 Response:

```bash
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

## 🛠️ Running the Service Locally

Spin it up in minutes! ⚡

#### 🐍 Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 📦 Install dependencies

```bash
pip install -r requirements.txt
```

#### 🚀 Launch the FastAPI server

```bsh
uvicorn main:app --reload
```

## 📁 Output Structure

After a successful job submission, the following directory will be generated:

```bash
jobs/{job_id}/
├── code/             # 📁 Cloned GitHub repository
├── data/             # 📂 Downloaded external dataset
├── run.sh            # 🖥️ Script to run the command
├── Dockerfile        # 🐳 Docker container specification
└── {job_id}.tar.gz   # 📦 Final packaged artifact
```

#### 🧪 You can inspect the `.tar.gz` file using:

```bash
tar -tf jobs/{job_id}.tar.gz
```

## 🐳 Docker Usage (Optional)

Want to run your job inside a container? No problem! 🧊

#### 🔓 Unpack the archive

```bash
tar -xzf jobs/{job_id}.tar.gz
cd {job_id}
```

#### 🏗️ Build the container

```bash
docker build -t packaged-job .
```

#### ▶️ Run it

```bsh
docker run --rm packaged-job
```

## 🔐 Security Note

All `.git/` directories are **automatically removed** after checkout to prevent leaking Git history or sensitive files. 🛡️

## 📐 Design Details

For more about the internal architecture and components of this service, check out the [Design Document](./DESIGN.md).

## 🙌 Contributing

Pull requests are welcome! For major changes, please open an issue first. 🤝
Let’s build safer, faster, and more reproducible pipelines together.

## 🧠 License

MIT License © 2025  
Made with ❤️ and FastAPI
