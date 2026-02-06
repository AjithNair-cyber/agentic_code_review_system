from langgraph.graph import StateGraph, END, START
from app.graph.agents.fan_out_agent_code_reviewer import dispatch_files
from app.graph.agents.github_diff_checker_agent import fetch_github_diff_agent
from app.graph.agents.reviewer_agent import code_reviewer_agent
from app.graph.state import GraphState

graph = StateGraph(GraphState)

# Nodes
graph.add_node("github_diff_checker", fetch_github_diff_agent)
graph.add_node("code_reviewer", code_reviewer_agent)

# Flow
graph.add_edge(START, "github_diff_checker")

# Fan-out routing
graph.add_conditional_edges(
    "github_diff_checker",
    dispatch_files
)

# After each reviewer finishes, go to END
graph.add_edge("code_reviewer", END)

app_graph = graph.compile()