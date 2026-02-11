import subprocess
from pathlib import Path
from app.graph.state import GraphState
import json
from app.helper_functions.pyright_functions import extract_pyright_errors
from app.helper_functions.logger_functions import logger


def github_code_cloning_agent_pyright(state: GraphState):   
    
    '''This agent clones the GitHub repository and checks out the specific branch and commit related to the recent code changes.
    It then runs Pyright on the cloned codebase to analyze it for type errors and other issues. 
    The Pyright error messages are extracted and stored in the state for further processing by the Pyright reviewer agent.
    It expects the state to have a "github" key with "owner", "repo", "after_sha", and "branch" information.
    The cloned repository is stored in a "repo_path" key in the state, and the Pyright error messages are stored in a "pyright_error_messages" key.
    As the github repo is needed for pyright analysis, the agent runs just after cloning and before any review agents and not seperately as another agent.'''
    
    if state["github"] is None:
        raise ValueError("GitHub information is missing from the state.")
   
    owner = state["github"]["owner"]
    repo_name = state["github"]["repo"]
    repo_url = f"https://github.com/{owner}/{repo_name}.git"
    branch = state["github"]["branch"]
    logger.info("[CLONE] Cloning repository for static analysis")
    logger.info(f"[CLONE] Repo: {repo_name}")
    
    if not repo_url or not branch:
        raise ValueError("Missing repo_url or branch_name")
    
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
        
        logger.info("[CLONE] Repository cloned successfully")

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

    logger.info(f"[PYRIGHT] Errors found: {len(pyright_output)}")
    return {
        "pyright_error_messages": pyright_output,
        "repo_path": str(repo_path)
    }
    