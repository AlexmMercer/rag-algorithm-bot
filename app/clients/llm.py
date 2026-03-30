import logging

from openai import AsyncOpenAI, InternalServerError, RateLimitError
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self, host: str, api_key: str, model: str, system_prompt: str):
        self._host = host
        self._api_key = api_key
        self._model = model
        self._system_prompt = system_prompt
        self._client = AsyncOpenAI(base_url=host, api_key=api_key)

    @retry(
        retry=retry_if_exception_type((RateLimitError, InternalServerError)),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        stop=stop_after_attempt(3),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    async def ask(self, question: str) -> str:
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": question},
            ],
        )
        return response.choices[0].message.content or ""
