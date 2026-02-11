from typing import TypedDict, List, Optional,Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
import operator

class PyrightErrorMessage(TypedDict):
    file: Optional[str]
    line: Optional[int]
    character: Optional[int]
    message: Optional[str]
    severity: Optional[str]
    rule: Optional[str]

class CodeReviewMessage(TypedDict):
    file: Optional[str]
    issue: Optional[str]
    line : Optional[int]
    character: Optional[int]
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
    
class ConsolidatedIssue(TypedDict):
    source: str  # "pyright" | "diff"
    message: Optional[str]
    line: Optional[int]
    character: Optional[int]
    severity: Optional[str]
    rule: Optional[str]
    recommended_fix: Optional[str]
    
class FileConsolidatedReview(TypedDict):
    file: str
    issues: List[ConsolidatedIssue]

class CodeWritterOutput(TypedDict):
    file : Optional[str]
    commit_message: Optional[str]
    updated_code: Optional[str]

class GraphState(TypedDict):

    # Conversation
    messages: Annotated[List[BaseMessage], add_messages]
    
   # GitHub metadata
    github: Optional[GitHubInfo]
    repo_path: Optional[str]
    
    # Code Diff
    diffset: Annotated[List[GithubDiffSet], operator.add]
    
    # Code Review Messages
    code_review_messages: Annotated[List[CodeReviewMessage], operator.add]
    
     # Pyright Error Messages
    pyright_error_messages: Annotated[List[PyrightErrorMessage], operator.add]
    
    # Pyright Review Messages
    pyright_review_messages: Annotated[List[CodeReviewMessage], operator.add]
    
    # Consolidated Reviews
    consolidated_reviews: Annotated[List[FileConsolidatedReview], operator.add]
    
    # Consolidated Code Updates after validation
    consolidated_code_updates: Annotated[List[CodeWritterOutput], operator.add]
    
    # Updated code after validation
    success: Optional[str]
    
    pr_url : Optional[str]
    
    # Report on code validati
    report: Optional[str]


