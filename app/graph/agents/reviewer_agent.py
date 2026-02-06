from langchain_core.prompts import ChatPromptTemplate
from app.graph.state import GraphState
from app.config.open_ai import open_ai_code_reviewer_client
from app.graph.prompts.SYSTEM_PROMPTS import REVIEWER_AGENT

def code_reviewer_agent(state: GraphState) :
    
    diff = state["diff"]
    
    prompt = ChatPromptTemplate.from_messages([
    ("system", REVIEWER_AGENT),
    ("human", "Diff: {diff}")
    ])
    
    chain = prompt | open_ai_code_reviewer_client
    
    result = chain.invoke({"diff": diff})
    print(f"Review Report: {result.content}...")  # Log first 100 chars of the report
    
    return {"code_review_messages": [result]}