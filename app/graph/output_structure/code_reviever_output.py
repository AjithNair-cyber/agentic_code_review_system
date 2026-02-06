from typing import TypedDict, Optional

class CodeDiffReviewMessage(TypedDict):
    file: Optional[str]
    issue: Optional[str]
    criticality: Optional[str]
    confidence: Optional[float]
    
    
class PyrightReviewMessage(TypedDict):
    file: Optional[str]
    issue: Optional[str]
    severity: Optional[str]
    recommended_fix: Optional[str]
    