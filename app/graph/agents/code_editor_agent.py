from app.graph.state import GraphState
from pathlib import Path
from app.helper_functions.logger_functions import logger

def write_to_file(state: GraphState):
    '''
    This agent takes the consolidated code updates and writes them to the respective files in the cloned repository.
    It expects the state to have a "consolidated_code_updates" key, which is a list of dictionaries with "file" and "updated_code" keys.
    '''  
    repo_path = state["repo_path"] or "workspaces"
    consolidated_code_updates = state["consolidated_code_updates"]
    if not consolidated_code_updates:
        return {"success": "No code updates to write."}
    
    logger.info("[EDITOR] Writing updated code to repository")
    
    for review in consolidated_code_updates:
        file_path = review["file"] or ""
        content = review["updated_code"] or ""
        file_path = Path(repo_path) / file_path
        update_required = review.get("update_required", True)
        logger.info(f"[EDITOR] Updated file: {file_path}")
        logger.info("[EDITOR] File write completed")
        if update_required:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
    
    return {"success": "All files updated successfully"}