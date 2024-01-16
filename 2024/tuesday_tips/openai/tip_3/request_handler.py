import asyncio
import math
from openai import AsyncOpenAI
from client import SYSTEM_MESSAGE
from tip_1.chunker import split_query_into_parts
from tip_1.encoding import get_number_of_tokens
from models import MODEL_TOKEN_LIMITS, OpenAIModels
from tip_2.rate_limiter import rate_limit
from tip_3.timer import timer



@rate_limit(max_calls=10, period=10)
async def send_request_async(query: str, model: OpenAIModels, client: AsyncOpenAI) -> str | None:

    response = await client.chat.completions.create(
        model=model.value,
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": query},
        ],
    )

    return response.choices[0].message.content 

@timer
async def handle_request(query: str, model: OpenAIModels, client: AsyncOpenAI) -> str:
    number_of_tokens: int = get_number_of_tokens(query, model)

    parts: list[str] = [query]
    if number_of_tokens > MODEL_TOKEN_LIMITS[model]:
        token_limit = math.floor(MODEL_TOKEN_LIMITS[model])
        parts = split_query_into_parts(query, token_limit)

    responses = await asyncio.gather(
        *(send_request_async(client=client, model=model, query=part) for part in parts)
    )
    return "".join(responses)

