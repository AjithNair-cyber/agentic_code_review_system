from langchain_core.prompts import ChatPromptTemplate
from app.graph.state import GraphState
from app.config.open_ai import open_ai_code_reviewer_client
from app.graph.prompts.SYSTEM_PROMPTS import REVIEWER_AGENT

def code_reviewer_agent(state: GraphState) :
    
    # Extract the code diff from the state
    diff = state["diffset"][0]
    
    prompt = ChatPromptTemplate.from_messages([
    ("system", REVIEWER_AGENT),
    ("human", "Diff: {diff}")
    ])
    
    chain = prompt | open_ai_code_reviewer_client
    
    result = chain.invoke({"diff": diff})
    
    return {"code_review_messages": [result]}