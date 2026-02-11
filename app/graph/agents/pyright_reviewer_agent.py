from langchain_core.prompts import ChatPromptTemplate
from app.graph.state import GraphState
from app.config.open_ai import open_ai_code_reviewer_client
from app.graph.prompts.SYSTEM_PROMPTS import PYRIGHT_REVIEWER_AGENT


async def pyright_reviewer_agent(state: GraphState):
    
    '''This agent reviews the Pyright error messages generated from the recent code changes and provides feedback on potential issues.
    It uses the PYRIGHT_REVIEWER_AGENT system prompt to instruct the AI on how to analyze the Pyright error messages and generate a review message.
    It expects the state to have a "pyright_error_messages" key, which is a list of Pyright error messages representing the issues found in the code analysis.
    The agent processes these error messages and generates a review message that is stored in the state under the "pyright_review_messages" key for further processing by the error aggregator agent.
    '''
    
    pyright_errors = state.get("pyright_error_messages")
    # Guard clause
    if not pyright_errors:
        return {"pyright_review_messages": []}
    
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