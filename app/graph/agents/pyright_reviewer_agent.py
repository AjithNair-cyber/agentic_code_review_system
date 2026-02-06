from langchain_core.prompts import ChatPromptTemplate
from app.graph.state import GraphState
from app.config.open_ai import open_ai_pyright_reviewer_client
from app.graph.prompts.SYSTEM_PROMPTS import GIT_DIFF_REVIEWER_AGENT


async def pyright_reviewer_agent(state: GraphState):
    pyright_error = state.get("pyright_error_messages")[0]
    print("Pyright Error to review:", pyright_error)
    prompt = ChatPromptTemplate.from_messages([
        ("system", GIT_DIFF_REVIEWER_AGENT),
        ("human", "Review this pyright error message:\n\n{pyright_report}")
    ])

    chain = prompt | open_ai_pyright_reviewer_client

    result = await chain.ainvoke({"pyright_report": pyright_error})

    return {
        "pyright_review_messages": [result]
    }