from app.graph.state import GraphState
from app.helper_functions.github_functions import fetch_github_diff, parse_diff

async def fetch_github_diff_agent(state: GraphState):
    g = state["github"]
    if not g:
        raise ValueError("GitHub information is missing from the state.")
    owner = g["owner"] or ""
    repo = g["repo"] or ""
    before_sha = g["before_sha"] or ""
    after_sha = g["after_sha"] or ""
    response = await fetch_github_diff(owner, repo, before_sha, after_sha)
    code_diff = parse_diff(response)
    return {"diffset": code_diff}