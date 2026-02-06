from langchain_core.prompts import ChatPromptTemplate
from app.graph.state import GraphState
from app.config.open_ai import open_ai_pyright_reviewer_client
from app.graph.prompts.SYSTEM_PROMPTS import GIT_DIFF_REVIEWER_AGENT


async def pyright_reviewer_agent(state: GraphState):
    pyright_report = state.get("pyright_report", "")

    prompt = ChatPromptTemplate.from_messages([
        ("system", GIT_DIFF_REVIEWER_AGENT),
        ("human", "Review this pyright report:\n\n{pyright_report}")
    ])

    chain = prompt | open_ai_pyright_reviewer_client

    result = await chain.ainvoke({"pyright_report": pyright_report})

    return {
        "code_review_messages": [result]
    }