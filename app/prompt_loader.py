from functools import lru_cache
from pathlib import Path


@lru_cache
def load_prompt(path: str) -> str:
    prompt_file = Path(path)
    if not prompt_file.is_file():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return prompt_file.read_text(encoding="utf-8").strip()
