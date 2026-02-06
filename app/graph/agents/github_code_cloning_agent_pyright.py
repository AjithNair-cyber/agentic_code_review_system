import subprocess
from pathlib import Path
from app.graph.state import GraphState


def github_code_cloning_agent_pyright(state: GraphState):
    owner = state["github"]["owner"]
    repo_name = state["github"]["repo"]
    repo_url = f"https://github.com/{owner}/{repo_name}.git"
    branch = state["github"]["branch"]
    if branch.startswith("refs/heads/"):
        branch = branch.replace("refs/heads/", "")
    after_sha = state["github"]["after_sha"]
    workspace_root = Path("workspaces")

    if not repo_url or not branch or not after_sha:
        raise ValueError("Missing repo_url, branch_name, or after_sha")

    # Unique folder per job
    repo_path = workspace_root / after_sha
    repo_path.mkdir(parents=True, exist_ok=True)

    try:
        # Clone specific branch shallow
        subprocess.run(
            [
                "git",
                "clone",
                "--depth", "1",
                "--branch", branch,
                repo_url,
                str(repo_path)
            ],
            check=True,
        )

        # Ensure exact commit
        subprocess.run(
            ["git", "fetch", "--depth", "1", "origin", after_sha],
            cwd=repo_path,
            check=True,
        )

        subprocess.run(
            ["git", "checkout", after_sha],
            cwd=repo_path,
            check=True,
        )

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git operation failed: {e}")

    return {
        "workspace_path": str(repo_path)
    }