from app.graph.state import GraphState
from pathlib import Path
import logging

def write_to_file(state: GraphState):
    repo_path = state["repo_path"] or "workspaces"
    consolidated_code_updates = state["consolidated_code_updates"]
    logging.info("Writing to file with repo_path: [REDACTED]")  # Avoid logging sensitive information
    logging.info("Consolidated code updates: " + str(consolidated_code_updates))
    if not consolidated_code_updates:
        return {"success": "No code updates to write."}
    
    for review in consolidated_code_updates:
        file_path = review["file"] or ""
        content = review["updated_code"] or ""
        file_path = Path(repo_path) / file_path
        logging.info(f"Writing to file: {file_path}")
        logging.info(f"Content:\n{content}")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
    
    return {"success": "All files updated successfully"}