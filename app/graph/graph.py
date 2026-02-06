from langgraph.graph import StateGraph, END, START
from app.graph.agents.reviewer_agent import code_reviewer_agent
from app.graph.agents.github_diff_checker_agent import fetch_github_diff_agent
from app.graph.state import GraphState

graph = StateGraph(GraphState)

graph.add_edge(START, "reviewer")
graph.add_node("reviewer", fetch_github_diff_agent)
graph.add_edge("reviewer", END)

app_graph = graph.compile()
