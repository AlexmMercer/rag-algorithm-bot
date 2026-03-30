from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    llm_host: str = Field(
        default="https://api.openai.com/v1", description="LLM API base URL"
    )
    llm_model: str = Field(default="gpt-4o-mini", description="LLM model name")
    llm_api_key: str = Field(default="", description="LLM API key")

    prompt_path: str = Field(
        default="prompts/default.txt",
        description="Path to the prompt template file",
    )


settings = Settings()
