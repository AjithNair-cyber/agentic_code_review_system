from app.graph.state import GraphState
from app.helper_functions.github_functions import fetch_github_diff, parse_diff
from app.helper_functions.logger_functions import logger

async def fetch_github_diff_agent(state: GraphState):
    '''
    This agent fetches the git diff of the recent code changes from GitHub using the GitHub API. 
    It expects the state to have a "github" key with "owner", "repo", "before_sha", and "after_sha" information. 
    The fetched diff is parsed and stored in the state under the "diffset" key for further processing by the diff checker reviewer agent.
    '''
    g = state["github"]
    if not g:
        raise ValueError("GitHub information is missing from the state.")
    owner = g["owner"] or ""
    repo = g["repo"] or ""
    before_sha = g["before_sha"] or ""
    after_sha = g["after_sha"] or ""
    response = await fetch_github_diff(owner, repo, before_sha, after_sha)
    code_diff = parse_diff(response)
    logger.info("[GITHUB_DIFF] Starting diff fetch")
    logger.info(f"[GITHUB_DIFF] Repo: {repo}")
    logger.info(f"[GITHUB_DIFF] Files changed: {len(code_diff)}")
    logger.info("[GITHUB_DIFF] Diff fetch completed")
    return {"diffset": code_diff}