from fastapi import APIRouter, Request
from app.graph.graph import app_graph
from app.graph.state import GraphState

router = APIRouter()

@router.post("/events")
async def handle_github_event(request: Request):
    payload = await request.json()
    # 1. Extract the 'before', 'after' SHAs, owner and github_repo from the payload
    before_sha = payload.get("before")
    after_sha = payload.get("after")
    owner = payload.get("repository").get('full_name').split('/')[0]
    repo = payload.get("repository").get('full_name').split('/')[1]
    branch = payload.get("ref")
    
    if not all([owner, repo, before_sha, after_sha]):
        raise ValueError("Missing required GitHub metadata")

    response = await app_graph.ainvoke(
        GraphState({
            "github": {
                "owner": owner,
                "repo": repo,
                "before_sha": before_sha,
                "after_sha": after_sha,
                "branch": branch
            },
            "messages": [],
            "diffset": [],
            "repo_path": "",
            "code_review_messages": [],
            "success": "",
            "report": "",
            "pyright_review_messages": [],
            "pyright_error_messages": [],
            "consolidated_reviews": [],
            "consolidated_code_updates": [],
            "pr_url": ""
        })
    )

    print("Graph Response:", response)
    
    return {"data": "Successfully processed GitHub event", "status": "success"}
