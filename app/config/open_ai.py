from langchain_openai import ChatOpenAI
from app.config.config import get_settings
from app.graph.state import CodeDiffReviewMessage, PyrightReviewMessage
from pydantic import SecretStr

settings = get_settings()

open_ai_client = ChatOpenAI(
    api_key=SecretStr(settings.OPEN_AI_API_KEY),
     model="gpt-4o-mini",
    temperature=0.7,
)

open_ai_diff_reviewer_client = open_ai_client.with_structured_output(CodeDiffReviewMessage)
open_ai_pyright_reviewer_client = open_ai_client.with_structured_output(PyrightReviewMessage)
