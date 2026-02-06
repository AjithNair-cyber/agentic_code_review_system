from langchain_openai import ChatOpenAI
from app.config.config import get_settings


settings = get_settings()

open_ai_client = ChatOpenAI(
    api_key=settings.OPEN_AI_API_KEY,
     model="gpt-4o-mini",
    temperature=0.7,
)
