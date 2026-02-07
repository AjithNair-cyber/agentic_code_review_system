from app.graph.state import GraphState
from pathlib import Path

def write_to_file(state: GraphState):
    repo_path = state["repo_path"] or "workspaces"
    file_path = state["consolidated_code_updates"]
    
    for review in state["consolidated_code_updates"]:
        file_path = review["file"] or ""
        content = review["updated_code"] or ""
        file_path = Path(repo_path) / file_path
        print(f"Writing to file: {file_path}")
        print(f"Content:\n{content}")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
    
    return {"success": "All files updated successfully"}