from langgraph.types import Send
from app.graph.state import GraphState

def send_individual_diff(state: GraphState):
    return [
        Send("diff_code_reviewer", {"diffset": [diff]})
        for diff in state["diffset"]
    ]