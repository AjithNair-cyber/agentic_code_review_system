from langgraph.graph import StateGraph, END, START
from app.graph.agents.reviewer_agent import code_reviewer_agent
from app.graph.agents.github_diff_checker_agent import fetch_github_diff_agent
from app.graph.state import GraphState

graph = StateGraph(GraphState)


graph.add_node("github_diff_checker", fetch_github_diff_agent)
graph.add_node("code_reviewer", code_reviewer_agent)


graph.add_edge(START, "github_diff_checker")
graph.add_edge("github_diff_checker", "code_reviewer")
graph.add_edge("code_reviewer", END)

app_graph = graph.compile()
