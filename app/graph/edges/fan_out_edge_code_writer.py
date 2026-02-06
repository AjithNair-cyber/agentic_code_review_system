from langgraph.types import Send
from app.graph.state import GraphState

def send_file_to_writer(state: GraphState):
    return [
        Send("code_writer", {"file_review": [review]})
        for review in state["consolidated_reviews"]
    ]