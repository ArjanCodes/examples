import math

from openai import OpenAI
from client import SYSTEM_MESSAGE
from tip_1.chunker import split_query_into_parts
from tip_1.encoding import get_number_of_tokens
from models import MODEL_TOKEN_LIMITS, OpenAIModels


def send_request(query: str, model: OpenAIModels, client: OpenAI) -> str | None:
    response = client.chat.completions.create(
        model=model.value,
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": query},
        ],
    )

    return response.choices[0].message.content


def handle_request(query: str, model: OpenAIModels, client: OpenAI) -> str:
    number_of_tokens: int = get_number_of_tokens(query, model)

    parts: list[str] = [query]
    if number_of_tokens > MODEL_TOKEN_LIMITS[model]:
        token_limit = math.floor(MODEL_TOKEN_LIMITS[model])
        parts = split_query_into_parts(query, token_limit)

    result = ""

    for part in parts:
        try:
            content = send_request(client=client, model=model, query=part)
            if content:
                result += content
        except Exception as e:
            print(f"An error occurred: {e}")

    return result
