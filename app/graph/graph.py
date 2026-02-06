from langgraph.graph import StateGraph, END, START
from app.graph.edges.fan_out_edge_code_reviewer import dispatch_files
from app.graph.agents.github_diff_checker_agent import fetch_github_diff_agent
from app.graph.agents.diff_checker_reviewer_agent import code_reviewer_agent
from app.graph.agents.github_code_cloning_agent_pyright import github_code_cloning_agent_pyright
from app.graph.agents.pyright_reviewer_agent import pyright_reviewer_agent
from app.graph.state import GraphState

graph = StateGraph(GraphState)

# Nodes
graph.add_node("github_diff_checker", fetch_github_diff_agent)
graph.add_node("github_code_cloning", github_code_cloning_agent_pyright)
graph.add_node("code_reviewer", code_reviewer_agent)
graph.add_node("pyright_reviewer", pyright_reviewer_agent)


# Flow
graph.add_edge(START, "github_diff_checker")
graph.add_edge(START, "github_code_cloning")
graph.add_edge("github_code_cloning", "pyright_reviewer")


# Fan-out routing
graph.add_conditional_edges(
    "github_diff_checker",
    dispatch_files
)

# After each reviewer finishes, go to END
graph.add_edge("code_reviewer", END)

app_graph = graph.compile()