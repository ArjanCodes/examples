from anyio import Path
from openai import OpenAI
from bragir.tracing.logger import logger
from bragir.file import calculate_file_size, process_file, remove_files

from bragir.timer import timing_decorator


@timing_decorator
def transcribe_audio_files(transcriber: OpenAI, audio_paths: list[str]) -> list[str]:
    return [transcribe_audio(transcriber, path) for path in audio_paths]


def transcribe_audio(client: OpenAI, audio_path: str) -> str:
    logger.info(f"Transcribing {audio_path}")
    transcript = client.audio.transcriptions.create(
        model="whisper-1", file=Path(audio_path), response_format="srt"
    )
    return transcript  # type:ignore


def transcribe_file(transcriber: OpenAI, path: str) -> list[str]:
    tmp_audio_paths: list[str] = []

    print("Transcribing file")

    try:
        file_size_mbytes = calculate_file_size(path)

        if file_size_mbytes < 25:
            return [transcribe_audio(transcriber, path)]

        tmp_audio_paths = [*tmp_audio_paths, *process_file(path)]

        return transcribe_audio_files(transcriber, tmp_audio_paths)
    finally:
        logger.info("Removing temporary files")
        remove_files(tmp_audio_paths)
