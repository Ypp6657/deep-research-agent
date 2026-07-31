from langchain_openai import ChatOpenAI

from config.settings import *


def get_llm(
    temperature: float = TEMPERATURE,
    max_tokens: int = MAX_TOKENS,
):
    return ChatOpenAI(
        model=MODEL_NAME,
        api_key=GPT_OSS_API_KEY,
        base_url=GPT_OSS_BASE_URL,
        temperature=temperature,
        max_tokens=max_tokens,
    )