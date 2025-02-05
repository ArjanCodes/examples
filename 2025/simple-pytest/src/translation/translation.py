import asyncio
from typing import Any

from openai import AsyncOpenAI, OpenAI
from pydantic import BaseModel

from src.config import get_config
from src.srt.srt_part import SRTPart
from src.timer import timing_decorator
from src.tracing.logger import logger


def split_by_breakpoints(
    collection: list[Any], breakpoints: list[int]
) -> list[list[Any]]:
    if len(collection) == 0 or len(collection) == 1:
        return collection

    result: list[Any] = []
    start_index = 0

    for breakpoint in breakpoints:
        result.append(collection[start_index:breakpoint])
        start_index = breakpoint

    # Append the remaining elements after the last breakpoint
    result.append(collection[start_index:])

    for res in result:
        if res == []:
            result.remove(res)

    return result


def translate(translator: OpenAI, part: SRTPart, language: str) -> str:
    completion = translator.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": f"""
                You are a translation machine that only translates text to **{language}**.

                Translate only into {language} without altering any other language.

                Index is the following: {part.index}
            """,
            },
            {"role": "user", "content": part.content},
        ],
        response_format=Part,
    )

    return completion.choices[0].message.content or ""


async def async_translate(translator: AsyncOpenAI, part: SRTPart, language: str) -> str:
    config = get_config()

    if config is None:
        raise Exception("Config not found")

    #    model = config.client.model

    completion = await translator.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": f"""
                You are a translation machine that only translates text to **{language}**.

                Translate only into {language} without altering any other language.

                Index is the following: {part.index}

                Only return me the translated text.
            """,
            },
            {"role": "user", "content": part.content},
        ],
        response_format=Part,
    )

    translated_part = completion.choices[0].message.parsed

    if translated_part is None:
        raise Exception("Translated part is None")

    return translated_part.content


async def translate_srt_part(
    translator: AsyncOpenAI,
    part: SRTPart,
    language: str,
) -> SRTPart:
    config = get_config()

    if config is None:
        raise Exception("Config not found")

    translation = await async_translate(translator, part, language)

    part.translation = translation

    return part


@timing_decorator
def translate_srt_parts(
    translator: OpenAI, parts: list[SRTPart], language: str
) -> list[SRTPart]:
    for i, part in enumerate(parts):
        part.translation = translate(translator, part, language)
        logger.info(f"Translated {i + 1}/{len(parts)}")

    return parts


async def async_translate_srt_parts(
    translator: AsyncOpenAI, srt_parts: list[SRTPart], language: str
) -> list[SRTPart]:
    tasks = [
        translate_srt_part(translator=translator, part=part, language=language)
        for part in srt_parts
    ]
    translated_parts = await asyncio.gather(*tasks)

    return translated_parts


class Part(BaseModel):
    index: int
    content: str
