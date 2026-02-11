# 🧠 Code Validator

## Agentic AI GitHub Code Review & Automated PR System

An AI-powered GitHub automation system built using **LangGraph** that
performs multi-stage code review, static analysis, automated fixes, PR
creation, and email notifications.

Instead of relying on a single LLM call, this system uses a structured
multi-agent workflow to simulate a real-world engineering review
pipeline.

---

## 🚀 What This Project Does

When a GitHub event is triggered:

1.  Fetches PR diff from GitHub\
2.  Clones the repository for static analysis\
3.  Performs LLM-based semantic code review\
4.  Runs Pyright type analysis\
5.  Aggregates errors per file\
6.  Generates corrected code\
7.  Writes changes directly to the repository\
8.  Raises a new PR with automated fixes\
9.  Sends an email notification with review summary

---

## 🏗 Architecture Overview

    GitHub Webhook
            ↓
          FastAPI
            ↓
         LangGraph

     ┌─────────────────────────────┐
     │ github_diff_checker         │
     │ github_code_cloning         │
     └────────────┬────────────────┘
                  ↓ (fan-out)
         diff_code_reviewer
         pyright_reviewer
                  ↓
           error_aggregator
                  ↓
             code_writer
                  ↓
             code_editor
                  ↓
              pr_raiser
                  ↓
            email_sender
                  ↓
                  END

---

## 🧩 Agents Explained

### 🔹 `github_diff_checker`

Fetches PR diff from GitHub webhook payload.

### 🔹 `github_code_cloning`

Clones the repository locally for static analysis.

### 🔹 `diff_code_reviewer`

LLM-based semantic code review agent.

### 🔹 `pyright_reviewer`

Runs static type analysis using Pyright.

### 🔹 `error_aggregator`

Groups errors by file and consolidates multi-source findings.

### 🔹 `code_writer`

Generates corrected code using LLM reasoning.

### 🔹 `code_editor`

Applies fixes directly to repository files.

### 🔹 `pr_raiser`

Creates a new PR with auto-generated fixes.

### 🔹 `email_sender`

Sends review summary via SMTP (MailHog for local testing).

---

## ⚙️ Tech Stack

- FastAPI\
- LangGraph (StateGraph)\
- OpenAI (GPT-4o-mini)\
- Pyright\
- Docker\
- MailHog (local SMTP testing)\
- GitHub Webhooks

---

## 🧠 Design Decisions

- Multi-agent architecture instead of a single LLM call for modular
  reasoning\
- Fan-out review pipeline to parallelize diff review and static
  analysis\
- Error aggregation stage to consolidate multi-source findings\
- Cost-efficient model choice (GPT-4o-mini) for production viability\
- Local email testing using MailHog to simulate production
  notifications

---

## 🛠 How to Run Locally

### 1️⃣ Clone Repository

    git clone <your-repo-url>
    cd <repo>

### 2️⃣ Create Virtual Environment

    python -m venv venv

    # Windows
    venv\Scripts\activate

    # macOS/Linux
    # source venv/bin/activate

    pip install -r requirements.txt

### 3️⃣ Start MailHog (Docker)

    docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog

Mail UI: http://localhost:8025

### 4️⃣ Run FastAPI Server

    uvicorn app.main:app

---

## 📬 Webhook Setup

- **Payload URL:** `http://your-domain/api/v1/github/events`\
- **Content Type:** `application/json`\
- **Trigger Events:** Push Events

---

## 👤 Author

**Ajith Nair**\
Full Stack Developer \| AI-Native Systems Enthusiast
