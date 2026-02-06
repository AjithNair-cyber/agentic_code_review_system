from langgraph.types import Send
from app.graph.state import GraphState

def send_individual_pyright_error(state: GraphState):
    return [
        Send("pyright_reviewer", {"pyright_error_messages": [error]})
        for error in state["pyright_error_messages"]
    ]