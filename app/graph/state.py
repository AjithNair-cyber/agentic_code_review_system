from typing import TypedDict, List, Optional,Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
import operator
    
    
class PyrightReviewMessage(TypedDict):
    files: Optional[List[str]]
    issue: Optional[str]
    severity: Optional[str]
    recommended_fix: Optional[str]

class GitHubInfo(TypedDict):
    owner: Optional[str]
    repo: Optional[str]
    before_sha: Optional[str]
    after_sha: Optional[str]
    branch: Optional[str]
    
class GithubDiffSet(TypedDict):
    path: Optional[str]
    status: Optional[str]
    added: Optional[List[str]]
    removed: Optional[List[str]]
    
class CodeDiffReviewMessage(TypedDict):
    file: Optional[str]
    issue: Optional[str]
    criticality: Optional[str]
    confidence: Optional[float]

class GraphState(TypedDict):

    # Conversation
    messages: Annotated[List[BaseMessage], add_messages]
    
    # Code review pyright 
    pyright_report: Optional[str]
    
   # GitHub metadata
    github: Optional[GitHubInfo]
    
    # Code Diff
    diffset: Annotated[List[GithubDiffSet], operator.add]
    
    # Code Review Messages
    code_review_messages: Annotated[List[CodeDiffReviewMessage], operator.add]
    
    # Pyright Review Messages
    pyright_review_messages: Optional[PyrightReviewMessage]
    
    # Updated code after validation
    suggested_code: Optional[str]
    
    # Report on code validation
    report: Optional[str]


