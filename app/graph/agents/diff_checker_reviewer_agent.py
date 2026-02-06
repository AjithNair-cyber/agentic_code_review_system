from langchain_core.prompts import ChatPromptTemplate
from app.graph.state import GraphState
from app.config.open_ai import open_ai_diff_reviewer_client
from app.graph.prompts.SYSTEM_PROMPTS import GIT_DIFF_REVIEWER_AGENT


async def code_reviewer_agent(state: GraphState):

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

    chain = prompt | open_ai_diff_reviewer_client

    result = await chain.ainvoke({"diff": formatted_diff})

    return {
        "code_review_messages": [result]
    }