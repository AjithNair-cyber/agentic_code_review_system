from collections import defaultdict
from app.graph.state import GraphState

def aggregate_reviews_by_file(state: GraphState):
    diff_reviews = state.get("code_review_messages", [])
    pyright_reviews = state.get("pyright_review_messages", [])

    grouped = defaultdict(list)
    print("Aggregating reviews by file " + str(len(diff_reviews)) + " diff reviews and " + str(len(pyright_reviews)) + " pyright reviews")
    print("Diff Reviews: " + str(diff_reviews))
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