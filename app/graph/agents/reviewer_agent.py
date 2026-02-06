from langchain_core.prompts import ChatPromptTemplate
from app.graph.state import GraphState
from app.config.open_ai import open_ai_code_reviewer_client
from app.graph.prompts.SYSTEM_PROMPTS import REVIEWER_AGENT


async def code_reviewer_agent(state: GraphState):

    diff = state["diffset"][0]
    pyright_report = state.get("pyright_report", "")

    formatted_diff = f"""
    File: {diff['path']}
    Status: {diff['status']}
    Added:
    {''.join(diff['added'] or [])}
    Removed:
    {''.join(diff['removed'] or [])}
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", REVIEWER_AGENT),
        ("human", "Review this git diff:\n\n{diff} and pyright report : {pyright_report}")
    ])

    chain = prompt | open_ai_code_reviewer_client

    result = await chain.ainvoke({"diff": formatted_diff, "pyright_report": pyright_report})

    return {
        "code_review_messages": [result]
    }