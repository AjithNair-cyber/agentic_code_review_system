from langgraph.types import Send
from app.graph.state import GraphState

def send_individual_diff(state: GraphState):
    diffs = state.get("diffset", [])
    if not diffs:
        # Force empty review so node runs
        return [Send("diff_code_reviewer", {"diff": None})]
    
    return [
        Send("diff_code_reviewer", {"diffset": [diff]})
        for diff in state["diffset"]
    ]