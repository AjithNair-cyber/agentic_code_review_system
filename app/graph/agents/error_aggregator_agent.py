from collections import defaultdict
from app.graph.state import GraphState

def aggregate_reviews_by_file(state: GraphState):
    
    '''
    This agent takes the individual code review messages from both the diff checker and the pyright reviewer and aggregates them by file.
    It expects the state to have "code_review_messages" and "pyright_review_messages" keys, which are lists of dictionaries with "file" and "message" keys.
    The output is a consolidated list of reviews for each file, which is stored in the "consolidated_reviews" key in the state.
    '''
    diff_reviews = state.get("code_review_messages", [])
    pyright_reviews = state.get("pyright_review_messages", [])

    grouped = defaultdict(list)
    # Merge both sources
    for review in diff_reviews:
        grouped[review["file"]].append({
            "source": "diff",
            **review
        })

    for error in pyright_reviews:
        grouped[error["file"]].append({
            "source": "pyright",
            **error
        })

    consolidated = [
        {
            "file": file,
            "issues": issues
        }
        for file, issues in grouped.items()
    ]    
    return {
        "consolidated_reviews": consolidated
    }