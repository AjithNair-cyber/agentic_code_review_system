import subprocess
import uuid
import httpx
from app.config.config import get_settings
from app.graph.state import GraphState


async def raise_pr_agent(state: GraphState):
    branch_name = f"ai-fix-{uuid.uuid4().hex[:6]}"
    settings = get_settings()
    GITHUB_TOKEN = settings.GITHUB_TOKEN
    print(GITHUB_TOKEN)
    github_info = state.get("github", {})

    if not github_info:
        print("GitHub information missing from state.")
        return {"pr_url": None}

    owner = github_info.get("owner")
    repo = github_info.get("repo")
    base_branch = github_info.get("branch", "main")
    repo_path = state.get("repo_path")

    if not repo_path:
        print("repo_path missing from state.")
        return {"pr_url": None}

    try:
        # Helper inline runner for better logs
        def run_git(cmd):
            print(f"\n🔹 Running: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                cwd=repo_path,
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                raise Exception(f"Git command failed: {' '.join(cmd)}")

            return result

        # 1️⃣ Create new branch
        
        run_git(["git", "checkout", "-b", branch_name])

        # 2️⃣ Add all changes
        run_git(["git", "add", "."])

        # 2. Add your identity (Standard practice for scripts)
        auth_url = f"https://x-access-token:{GITHUB_TOKEN}@github.com/{owner}/{repo}.git"
        run_git(["git", "remote", "set-url", "origin", auth_url])
        # 3️⃣ Commit
        run_git(["git", "commit", "-m", "AI Automated Code Fix"])

        # 4️⃣ Push branch
        run_git([ "git","push","--set-upstream","origin", branch_name])  

        # 5️⃣ Create PR via API
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.github.com/repos/{owner}/{repo}/pulls",
                headers=headers,
                json={
                    "title": "AI Automated Fix",
                    "body": "This PR was generated automatically.",
                    "head": branch_name,
                    "base": base_branch
                }
            )

        if response.status_code >= 400:
            print("\n❌ GitHub API Error")
            print("Status Code:", response.status_code)
            print("Response:", response.text)
            return {"pr_url": None}

        pr_url = response.json().get("html_url")
        print("\n✅ PR Created:", pr_url)

        return {"pr_url": pr_url}

    except Exception as e:
        print("\n❌ Exception in raise_pr_agent:")
        print(str(e))
        return {"pr_url": None}