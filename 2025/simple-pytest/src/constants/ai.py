from typing import get_args
from openai.types import ChatModel


MODEL_TOKEN_LIMITS = {
    "gpt-4o": 128000,
    "gpt-4o-2024-08-06": 128000,
    "gpt-4o-mini": 128000,
    "gpt-4o-mini-2024-07-18": 128000,
    "gpt-4o-realtime-preview": 128000,
    "gpt-4o-audio-preview": 128000,
    "o1-preview": 128000,
    "o1-preview-2024-09-12": 128000,
    "o1-mini": 128000,
    "o1-mini-2024-09-12": 128000,
    "gpt-4-turbo": 128000,
    "gpt-4": 8192,
    "gpt-3.5-turbo": 16385,
}


POSSIBLE_MODELS: list[str] = list(get_args(ChatModel))


def get_model_limit(model: str) -> int | None:
    if model not in POSSIBLE_MODELS:
        return None

    return MODEL_TOKEN_LIMITS.get(model, 128000)
