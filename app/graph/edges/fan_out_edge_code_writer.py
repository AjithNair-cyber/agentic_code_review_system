from langgraph.types import Send
from app.graph.state import GraphState

def send_file_to_writer(state: GraphState):
    repo_data = {"repo_path" : state["repo_path"]}
    consolidated_reviews = state.get("consolidated_reviews", [])
    if not consolidated_reviews:
        # Force empty review so node runs
        return [Send("code_writer", {**repo_data, "consolidated_reviews": []})]
    return [
        Send("code_writer", {**repo_data, "consolidated_reviews": [review]})
        for review in state["consolidated_reviews"]
    ]