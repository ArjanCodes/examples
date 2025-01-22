import asyncio

from anyio import Path
from openai import AsyncOpenAI, OpenAI

from bragir.file import calculate_file_size, process_file, remove_files
from bragir.timer import timing_decorator
from bragir.tracing.logger import logger


async def async_transcribe_audio(client: AsyncOpenAI, audio_path: str) -> str:
    logger.info(f"Transcribing {audio_path}")
    transcript = await client.audio.transcriptions.create(
        model="whisper-1", file=Path(audio_path), response_format="srt"
    )
    return transcript


def transcribe_audio(client: OpenAI, audio_path: str) -> str:
    logger.info(f"Transcribing {audio_path}")
    transcript = client.audio.transcriptions.create(
        model="whisper-1", file=Path(audio_path), response_format="srt"
    )
    return transcript


async def async_transcribe_audio_files(
    transcriber: AsyncOpenAI, audio_paths: list[str]
) -> list[str]:
    tasks = [async_transcribe_audio(transcriber, path) for path in audio_paths]
    return await asyncio.gather(*tasks)


@timing_decorator
def transcribe_audio_files(transcriber: OpenAI, audio_paths: list[str]) -> list[str]:
    return [transcribe_audio(transcriber, path) for path in audio_paths]


async def async_transcribe_file(transcriber: AsyncOpenAI, path: str) -> list[str]:
    tmp_audio_paths: list[str] = []

    try:
        file_size_mbytes = calculate_file_size(path)

        if file_size_mbytes < 25:
            return [await async_transcribe_audio(transcriber, path)]

        tmp_audio_paths = [*tmp_audio_paths, *process_file(path)]

        return await async_transcribe_audio_files(transcriber, tmp_audio_paths)
    finally:
        logger.info("Removing temporary files")
        remove_files(tmp_audio_paths)


def transcribe_file(transcriber: OpenAI, path: str) -> list[str]:
    tmp_audio_paths: list[str] = []

    try:
        file_size_mbytes = calculate_file_size(path)

        if file_size_mbytes < 25:
            return [transcribe_audio(transcriber, path)]

        tmp_audio_paths = [*tmp_audio_paths, *process_file(path)]

        return transcribe_audio_files(transcriber, tmp_audio_paths)
    finally:
        logger.info("Removing temporary files")
        remove_files(tmp_audio_paths)
