from typing import TypedDict, Optional

class CodeReviewMessage(TypedDict):
    file: Optional[str]
    issue: Optional[str]
    criticality: Optional[str]
    confidence: Optional[float]