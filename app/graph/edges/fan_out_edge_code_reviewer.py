from langgraph.types import Send
from app.graph.state import GraphState

def dispatch_files(state: GraphState):
    return [
        Send("code_reviewer", {"diffset": [diff]})
        for diff in state["diffset"]
    ]