from langchain_openai import ChatOpenAI
from app.config.config import get_settings
from app.graph.output_structure.code_reviever_output import CodeReviewMessage


settings = get_settings()

open_ai_client = ChatOpenAI(
    api_key=settings.OPEN_AI_API_KEY,
     model="gpt-4o-mini",
    temperature=0.7,
)

open_ai_code_reviewer_client = open_ai_client.with_structured_output(CodeReviewMessage)
