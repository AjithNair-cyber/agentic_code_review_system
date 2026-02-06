from app.graph.state import GraphState

def dispatch_files(state: GraphState):
    return [
        {"diffset": [diff]}
        for diff in state["diffset"]
    ]