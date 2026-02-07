from langgraph.types import Send
from app.graph.state import GraphState

def send_individual_pyright_error(state: GraphState):
    pyright_errors = state.get("pyright_error_messages", [])
    if not pyright_errors:
        # Force empty review so node runs
        return [Send("pyright_reviewer", {"pyright_error_messages": []})]
    return [
        Send("pyright_reviewer", {"pyright_error_messages": [error]})
        for error in state["pyright_error_messages"]
    ]