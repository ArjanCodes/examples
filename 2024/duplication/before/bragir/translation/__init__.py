from typing import Any
from openai import OpenAI

from bragir.files.file import File
from bragir.tracing.logger import logger
from bragir.timer import timing_decorator


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


def translate_content(client: OpenAI, text: str, language: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": f"You are a translator machine, you can only translate to the following language {language}. You need to keep the exact same format as the file. only translate the pieces of text. Make sure that all the text is translated and that there are no timestamps missing. Don't add any whitespace on the first line of the file or the last line of the file",
            },
            {"role": "user", "content": text},
        ],
    )

    return completion.choices[0].message.content or ""


@timing_decorator
def translate_srt(translator: OpenAI, file: File, language: str) -> str:
    logger.info(f"Translating {file.source_path} to {language}")

    translated_text = ""

    if len(file.breakpoints) == 0:
        translated_text += translate_content(translator, file.contents, language)

    if len(file.breakpoints) > 0:
        chunks = split_by_breakpoints(file.SRTParts, breakpoints=file.breakpoints)

        for i, chunk in enumerate(chunks):
            text = ""
            for part in chunk:
                text += part.srt_format
            text.rstrip("\n")

            translated_text += translate_content(translator, text, language)

            # Add new block onto the text
            translated_text += "\n\n"

            logger.info(f"Chunk {i + 1} translated")

    logger.info(f"Translated {file.source_path} to {language}")
    return translated_text
