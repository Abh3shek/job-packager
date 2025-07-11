# 🧠 Design Document: Asynchronous Job Execution Packager

This document explains the **architecture**, **workflow**, **security design**, and **reproducibility strategy** for the asynchronous job packaging system.

---

## 🗂️ Overview

The service securely packages arbitrary code and data for **reproducible execution** inside a containerized environment. It ensures that a specific code commit, dataset, and command can be **re-executed identically** across different systems.

---

## 🖼️ System Architecture Diagram

![Architecture Diagram](flowchart.svg)

## 🔁 Component Flow

### 📤 1. Client Submits Job

- Contains: `git_url`, `commit_hash`, `data_url`, and `command`

### 🧬 2. Clone Git Repo

- Checks out the specified commit using **GitPython**

- `.git/` directory is removed after cloning to eliminate sensitive history

## 📥 3. Download Data File

- Downloads file from `data_url` using `requests`

- Stored in a local `data/` directory

## 🛠️ 4. Generate Scripts

- `run.sh` is created to execute the provided command within `/code`

- A `Dockerfile` is generated to define the container environment

## 📦 5. Package Artifact

- Entire job directory is compressed into a reproducible `.tar.gz` bundle

## 🔐 Security Considerations

| 🛡️ **Risk**               | ✅ **Mitigation**                                          |
| ------------------------- | ---------------------------------------------------------- |
| Arbitrary Git URLs        | Validate & restrict with firewall rules in production      |
| Dangerous Commands        | Run jobs inside isolated containers _(future enhancement)_ |
| Sensitive data in `.git/` | `.git/` folder is deleted after cloning                    |
| Malicious data URLs       | Use timeouts, restrict allowed domains, or proxy requests  |

## 📦 Why This Is Reproducible

- 🔒 Code is pinned to a specific `commit_hash`

- 🌐 Data is downloaded at runtime and stored locally

- ⚙️ Both `run.sh` and `Dockerfile` are auto-generated and version-controlled

- 📦 The entire job is packaged into a `.tar.gz` archive

➡️ Same input always yields the same output

## 🧪 Example Output Directory Structure

```bash
jobs/
└── 123e4567-e89b-12d3-a456-426614174000/
    ├── code/
    ├── data/
    ├── run.sh
    ├── Dockerfile
    └── 123e4567-e89b-12d3-a456-426614174000.tar.gz
```

## ⚙️ Technologies Used

- 🐍 Python 3.12

- ⚡ FastAPI

- 🧬 GitPython

- 🌐 Requests

- 🐳 Docker

- 📦 tarfile (Python built-in)

## 📌 Future Enhancements

- 🧵 Add queue system to dispatch and execute packaged jobs

- 🔐 Support authenticated Git URLs

- 🧰 Validate commands against a safe-list

- 📢 Webhook notification when jobs are completed

## 📬 Contact

Created as part of AryaXAI backend internship assignment.
See [README.md](./README.md) for installation and usage instructions.
