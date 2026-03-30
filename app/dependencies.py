from functools import lru_cache
from pathlib import Path

from app.clients.llm import LLMClient
from app.settings import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_llm_client() -> LLMClient:
    settings = get_settings()
    system_prompt_path = Path(settings.prompt_path)
    if not system_prompt_path.is_file():
        raise FileNotFoundError(f"System prompt file not found: {settings.prompt_path}")
    system_prompt = system_prompt_path.read_text(encoding="utf-8")
    return LLMClient(
        host=settings.llm_host,
        api_key=settings.llm_api_key,
        model=settings.llm_model,
        system_prompt=system_prompt,
    )
