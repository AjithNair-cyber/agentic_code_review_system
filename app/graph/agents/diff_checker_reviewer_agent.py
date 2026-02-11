from langchain_core.prompts import ChatPromptTemplate
from app.graph.state import GraphState
from app.config.open_ai import open_ai_code_reviewer_client
from app.graph.prompts.SYSTEM_PROMPTS import GIT_DIFF_REVIEWER_AGENT


async def code_reviewer_agent(state: GraphState):
    '''
    This agent reviews the git diff of the recent code changes and provides feedback on potential issues. It uses the GIT_DIFF_REVIEWER_AGENT system prompt to instruct the AI on how to analyze the diff and generate a review message.
    It expects the state to have a "diffset" key, which is a list of dictionaries with "path", "status", "added", and "removed" keys representing the file changes in the git diff.
    '''
    diffset = state.get("diffset")

    # Guard clause
    if not diffset:
        print("No diffset. Skipping reviewer.")
        return {"code_review_messages": []}

    diff = state["diffset"][0]
    formatted_diff = f"""
    File: {diff['path']}
    Status: {diff['status']}
    Added:
    {''.join(diff['added'] or [])}
    Removed:
    {''.join(diff['removed'] or [])}
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", GIT_DIFF_REVIEWER_AGENT),
        ("human", "Review this git diff:\n\n{diff}")
    ])

    chain = prompt | open_ai_code_reviewer_client

    result = await chain.ainvoke({"diff": formatted_diff})

    return {
        "code_review_messages": [result]
    }