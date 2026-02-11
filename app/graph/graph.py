from langgraph.graph import StateGraph, END, START
from app.graph.edges.fan_out_edge_code_reviewer import send_individual_diff
from app.graph.edges.fan_out_edge_pyright_reviewer import send_individual_pyright_error
from app.graph.edges.fan_out_edge_code_writer import send_file_to_writer
from app.graph.agents.github_diff_checker_agent import fetch_github_diff_agent
from app.graph.agents.diff_checker_reviewer_agent import code_reviewer_agent
from app.graph.agents.github_code_cloning_agent_pyright import github_code_cloning_agent_pyright
from app.graph.agents.pyright_reviewer_agent import pyright_reviewer_agent
from app.graph.agents.error_aggregator_agent import aggregate_reviews_by_file
from app.graph.agents.coder_agent import senior_coder_agent
from app.graph.agents.code_editor_agent import write_to_file
from app.graph.agents.pr_raising_agent import raise_pr_agent
from app.graph.agents.email_sending_agent import email_agent
from app.graph.state import GraphState


graph = StateGraph(GraphState)

# Nodes
graph.add_node("github_diff_checker", fetch_github_diff_agent)
graph.add_node("github_code_cloning", github_code_cloning_agent_pyright)
graph.add_node("diff_code_reviewer", code_reviewer_agent)
graph.add_node("pyright_reviewer", pyright_reviewer_agent)
graph.add_node("error_aggregator", aggregate_reviews_by_file)
graph.add_node("code_writer", senior_coder_agent)
graph.add_node("code_editor", write_to_file)
graph.add_node("pr_raiser", raise_pr_agent)
graph.add_node("email_sender", email_agent)

# Flow
graph.add_edge(START, "github_diff_checker")
graph.add_edge(START, "github_code_cloning")


# Fan-out routing
graph.add_conditional_edges(
    "github_diff_checker",
    send_individual_diff
)
graph.add_conditional_edges(
    "github_code_cloning",
    send_individual_pyright_error
)


# After reviewer finishes, go to error aggregator
graph.add_edge(
    ["diff_code_reviewer", "pyright_reviewer"],
    "error_aggregator"
)

graph.add_conditional_edges(
    "error_aggregator",
    send_file_to_writer)

# After error aggregation, go to END
graph.add_edge("code_writer", "code_editor")
graph.add_edge("code_editor", "pr_raiser")
graph.add_edge("pr_raiser", "email_sender")
graph.add_edge("email_sender", END)

app_graph = graph.compile()