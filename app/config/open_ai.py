from langchain_openai import ChatOpenAI
from app.config.config import get_settings
from pydantic import SecretStr


settings = get_settings()

open_ai_client = ChatOpenAI(
    api_key=SecretStr(settings.OPEN_AI_API_KEY),  # Wrap the string in SecretStr
    model="gpt-4",
    temperature=0.7,
)