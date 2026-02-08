import subprocess
import uuid
import httpx
from app.config.config import get_settings
from app.graph.state import GraphState

async def raise_pr_agent(state: GraphState):
    branch_name = f"ai-fix-{uuid.uuid4().hex[:6]}"
    settings = get_settings()
    GITHUB_TOKEN = settings.GITHUB_TOKEN
    github_info = state.get("github", {})
    
    if github_info is None:
        print("GitHub information is missing from the state. Cannot raise PR.")
        return {"pr_url": None}
    
    owner = github_info.get("owner")
    repo = github_info.get("repo")
    base_branch = github_info.get("branch", "main")

    try:
        # 1️⃣ Create new branch
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)

        # 2️⃣ Add all changes
        subprocess.run(["git", "add", "."], check=True)

        # 3️⃣ Commit
        subprocess.run(
            ["git", "commit", "-m", "AI Automated Code Fix"],
            check=True
        )

        # 4️⃣ Push branch
        subprocess.run(
            ["git", "push", "origin", branch_name],
            check=True
        )
        
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

        response.raise_for_status()

        return {
            "pr_url": response.json()["html_url"]
        }

    except subprocess.CalledProcessError as e:
        print("Git operation failed:", e)
        return {}