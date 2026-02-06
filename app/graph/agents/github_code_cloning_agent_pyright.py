import subprocess
from pathlib import Path
from app.graph.state import GraphState
import json
from app.helper_functions.pyright_functions import extract_pyright_errors


def github_code_cloning_agent_pyright(state: GraphState):
    owner = state["github"]["owner"]
    repo_name = state["github"]["repo"]
    repo_url = f"https://github.com/{owner}/{repo_name}.git"
    branch = state["github"]["branch"]
    if branch.startswith("refs/heads/"):
        branch = branch.replace("refs/heads/", "")
    after_sha = state["github"]["after_sha"]

    if not repo_url or not branch or not after_sha:
        raise ValueError("Missing repo_url, branch_name, or after_sha")

    workspace_root = Path("workspaces")
    repo_path = workspace_root / after_sha
    pyright_output = ''

    repo_path.mkdir(parents=True, exist_ok=True)

    try:
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

        # ---------------------------
        # 🔥 CREATE PYRIGHT CONFIG
        # ---------------------------
        pyright_config = {
            "typeCheckingMode": "basic",
            "reportMissingImports": False,
            "reportMissingModuleSource": False,
            "exclude": [
                "**/__pycache__",
                "**/venv",
                "**/.venv",
                "**/node_modules"
            ]
        }

        with open(repo_path / "pyrightconfig.json", "w") as f:
            json.dump(pyright_config, f)

        # ---------------------------
        # 🔥 RUN PYRIGHT
        # ---------------------------
        result = subprocess.run(
            ["pyright", "--outputjson"],
            cwd=repo_path,
            capture_output=True,
            text=True,
        )
        
        pyright_json = json.loads(result.stdout)
        
        pyright_output = extract_pyright_errors(pyright_json)

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git operation failed: {e}")

    return {
        "pyright_error_messages": pyright_output
    }
    