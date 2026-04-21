from functools import lru_cache

from app.clients.llm import LLMClient
from app.prompt_loader import load_prompt
from app.settings import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_llm_client() -> LLMClient:
    settings = get_settings()
    system_prompt = load_prompt(settings.prompt_path)
    return LLMClient(
        host=settings.llm_host,
        api_key=settings.llm_api_key,
        model=settings.llm_model,
        system_prompt=system_prompt,
    )
