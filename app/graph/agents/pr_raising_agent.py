import subprocess
import uuid
import httpx
from app.config.config import get_settings
from app.graph.state import GraphState
from app.helper_functions.logger_functions import logger


async def raise_pr_agent(state: GraphState):
    
    '''This agent takes the consolidated code updates and creates a new branch in the GitHub repository, commits the changes, pushes the branch,
    and then creates a pull request via the GitHub API.
    It expects the state to have a "github" key with "owner", "repo", and "branch" information, as well as a "repo_path" key to locate the 
    cloned repository and a "consolidated_code_updates" key with the commit messages for the PR.
    The generated PR URL is stored in the "pr_url" key in the state for further processing by the email sending agent.
    Currently uses the local Git CLI for git operations and httpx for the GitHub API call.'''
    
    branch_name = f"ai-fix/{uuid.uuid4().hex[:6]}"
    settings = get_settings()
    GITHUB_TOKEN = settings.GITHUB_TOKEN
    # Removed the print statement that exposes GITHUB_TOKEN
    github_info = state.get("github", {})
    commit_messages = state.get("consolidated_code_updates", [])
    commit_message = "AI Automated Code Fix"
    for msg in commit_messages:
        commit_message += f"\n{msg.get('commit_message', '')}"

    if not github_info:
        return {"pr_url": None}

    owner = github_info.get("owner")
    repo = github_info.get("repo")
    base_branch = github_info.get("branch", "main")
    repo_path = state.get("repo_path")

    if not repo_path:
        return {"pr_url": None}
    
    logger.info("[PR] Creating automated fix PR")
    logger.info(f"[PR] Base branch: {base_branch}")


    try:
        # Helper inline runner for better logs
        def run_git(cmd):
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
        run_git(["git", "commit", "-m", commit_message])

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
            logger.error(f"GitHub API Error: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return {"pr_url": None}

        pr_url = response.json().get("html_url")
        logger.info(f"✅ PR Created: {pr_url}")

        return {"pr_url": pr_url}

    except Exception as e:
        logger.error(f"❌ Exception in raise_pr_agent: {str(e)}")
        return {"pr_url": None}