from fastapi import APIRouter, Request
from app.graph.graph import app_graph


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

    response = await app_graph.ainvoke({
        "github": {
            "owner": owner,
            "repo": repo,
            "before_sha": before_sha,
            "after_sha": after_sha,
            "branch": branch
        }
    })

    print("Graph Response:", response)
    
    return {"data": "Successfully processed GitHub event", "status": "success"}
