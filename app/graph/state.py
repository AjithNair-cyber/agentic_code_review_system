from typing import TypedDict, List, Optional,Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
import operator


class GitHubInfo(TypedDict):
    owner: Optional[str]
    repo: Optional[str]
    before_sha: Optional[str]
    after_sha: Optional[str]
    
class GithubDiffSet(TypedDict):
    path: Optional[str]
    status: Optional[str]
    added: Optional[List[str]]
    removed: Optional[List[str]]

class GraphState(TypedDict):

    # Conversation
    messages: Annotated[List[BaseMessage], add_messages]
    
   # GitHub metadata
    github: Optional[GitHubInfo]
    
    # Code Diff
    diffset: Annotated[List[GithubDiffSet], operator.add]
    
    # Updated code after validation
    suggested_code: Optional[str]
    
    # Report on code validation
    report: Optional[str]


