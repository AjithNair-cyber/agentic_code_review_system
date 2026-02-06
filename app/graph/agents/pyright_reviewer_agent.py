from langchain_core.prompts import ChatPromptTemplate
from app.graph.state import GraphState
from app.config.open_ai import open_ai_code_reviewer_client
from app.graph.prompts.SYSTEM_PROMPTS import PYRIGHT_REVIEWER_AGENT


async def pyright_reviewer_agent(state: GraphState):
    pyright_error = state.get("pyright_error_messages")[0]
    prompt = ChatPromptTemplate.from_messages([
        ("system", PYRIGHT_REVIEWER_AGENT),
        ("human", "Review this pyright error message:\n\n{pyright_report}")
    ])

    chain = prompt | open_ai_code_reviewer_client

    result = await chain.ainvoke({"pyright_report": pyright_error})

    return {
        "pyright_review_messages": [result]
    }