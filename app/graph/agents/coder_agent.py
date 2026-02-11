from app.graph.state import GraphState
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from app.graph.prompts.SYSTEM_PROMPTS import CODE_WRITER_AGENT
from app.config.open_ai import open_ai_code_writer_client
from app.helper_functions.logger_functions import logger

async def senior_coder_agent(state:GraphState):
    '''
    This agent takes the consolidated reviews and writes code updates for each file.
    It uses the CODE_WRITER_AGENT system prompt to instruct the AI on how to generate the updated code based on the original file content and the list of issues.
    It expects the state to have a "consolidated_reviews" key, which is a list of dictionaries with "file" and "issues" keys.
    It also expects a "repo_path" key to locate the files in the cloned repository.'''
    
    consolidated_reviews = state["consolidated_reviews"]
    
    if not consolidated_reviews:
        return {"consolidated_code_updates": []}
    
    consolidated_review = consolidated_reviews[0]
    repo_path = state["repo_path"] or "workspaces"
    file_path = consolidated_review["file"]
    file_path = Path(repo_path) / file_path
    
    logger.info("[WRITER] Generating fixes using LLM")
    logger.info(f"[WRITER] Fixing file: {file_path}")
    
    file_content = file_path.read_text(encoding="utf-8")
    issues = consolidated_review["issues"]
    code_changes_required = any(issue.get("code_change_required", False) for issue in issues)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", CODE_WRITER_AGENT),
        ("human", "Content:\n{content}\nIssues:\n{issues}")
    ])

    chain = prompt | open_ai_code_writer_client

    if(not code_changes_required):
        logger.info("[WRITER] No code changes required for this file.")
        result = {
            "file": file_path,
            "updated_code": file_content,
            "commit_message": f"No changes required for {file_path}"
        }
    else:
        result = await chain.ainvoke({ "content": file_content, "issues": issues})
    
    logger.info("[WRITER] Code generation completed")
    
    return {
        "consolidated_code_updates": [result]
        }
    