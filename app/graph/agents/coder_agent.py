from app.graph.state import GraphState
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from app.graph.prompts.SYSTEM_PROMPTS import CODE_WRITER_AGENT
from app.config.open_ai import open_ai_code_writter_client

async def senior_coder_agent(state:GraphState):
    consolidated_review = state["consolidated_reviews"][0]
    repo_path = state.get("repo_path", "workspaces")
    file_path = consolidated_review["file"]
    file_path = Path(repo_path) / file_path
    
    file_content = file_path.read_text(encoding="utf-8")
    issues = consolidated_review["issues"]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", CODE_WRITER_AGENT),
        ("human", "Content:\n{content}\nIssues:\n{issues}")
    ])

    chain = prompt | open_ai_code_writter_client

    result = await chain.ainvoke({ "content": file_content, "issues": issues})
    
    return {
        "consolidated_code_updates": [result]}
    