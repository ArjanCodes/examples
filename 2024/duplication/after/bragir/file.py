import os

import click

from bragir.audio.chunking import chunk_audio
from bragir.constants import TOKEN_LIMIT
from bragir.files.file import File
from bragir.languages import Languages
from bragir.srt.srt_part import SRTPart
from bragir.tracing.logger import logger


def calculate_duration_ms(file_size_mb: int, bitrate_kbps: int) -> float:
    file_size_bits = file_size_mb * 8 * 1024 * 1024  # Convert MB to bits
    duration_ms = (
        file_size_bits / bitrate_kbps
    ) * 1000  # Calculate duration in milliseconds
    return duration_ms


def calculate_file_size(file_path: str) -> float:
    file_size_bytes = os.path.getsize(file_path)
    return file_size_bytes / (1024 * 1024)


def read_file(file_path: str):
    with open(file_path, "r") as file:
        file_content = file.read()
    return file_content


def create_file(file: File, content: str):
    with open(file.target_path, "a+", encoding="utf-8") as fileIO:
        fileIO.write(content)


def get_new_file_path(file: str, target_language: Languages) -> str:
    base_path, file_name = os.path.split(file)
    updated_file_name = f"{target_language.value.lower()[:3]}_{file_name}"
    new_file_path = os.path.join(base_path, updated_file_name)
    return new_file_path


def chunk_content_into_srt_parts(content: str) -> list[SRTPart]:
    blocks = content.strip().split("\n\n")

    SRTParts: list[SRTPart] = []

    for block in blocks:
        lines = block.split("\n")

        number = int(lines[0])
        times = lines[1].split(" --> ")
        start_time, end_time = times[0], times[1]
        text = " ".join(lines[2:])

        SRTParts.append(
            SRTPart(
                index=number,
                start_time=start_time,
                end_time=end_time,
                content=text,
                source=block,
            )
        )

    return SRTParts


def get_breakpoints(SRTParts: list[SRTPart]) -> list[int]:
    buffer_limit: int = TOKEN_LIMIT
    buffer = 0

    breakpoints: list[int] = []

    for i, strpart in enumerate(SRTParts):
        buffer += strpart.number_of_tokens

        if buffer > buffer_limit:
            prev_srt_part = SRTParts[i - 1]
            next_srt_part = strpart

            breakpoints.append(i)

            sentences: list[str] = prev_srt_part.content.split(".")

            last_sentence = sentences[-1]

            prev_srt_part.content = "".join(prev_srt_part.content.split(".")[:-1])

            next_srt_part.content = last_sentence + " " + next_srt_part.content

            buffer = 0

    return breakpoints


def chunk_content(file_content: str) -> tuple[list[SRTPart], list[int]]:
    srt_parts: list[SRTPart] = chunk_content_into_srt_parts(file_content)

    breakpoints: list[int] = get_breakpoints(srt_parts)

    return (srt_parts, breakpoints)


def construct_target_files_for_path(
    path: str, languages: list[Languages]
) -> list[File]:
    files: list[File] = []

    for target_language in languages:
        file_content = read_file(path)
        (srt_parts, breakpoints) = chunk_content(file_content)
        target_path = get_new_file_path(path, target_language)

        files.append(
            File(
                name=path,
                contents=file_content,
                language=target_language,
                SRTParts=srt_parts,
                breakpoints=breakpoints,
                target_path=target_path,
                source_path=path,
            )
        )

    return files


def process_files(file_paths: list[str], languages: list[Languages]) -> list[File]:
    processed_files: list[File] = []
    for file_path in file_paths:
        processed_files.extend(construct_target_files_for_path(file_path, languages))

    return processed_files


def process_file(file_path: str) -> list[str]:
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower().replace(".", "")

    chunks = chunk_audio(file_path, format=file_extension)
    directory, base_name = os.path.split(file_path)

    chunk_paths: list[str] = []
    for i, chunk in enumerate(chunks):
        new_base_name = f"{i}_{base_name}"
        new_path = os.path.join(directory, new_base_name)
        chunk.export(new_path, format=file_extension)  # type:ignore
        chunk_paths.append(new_path)  # type:ignore

    return chunk_paths


def remove_files(file_paths: list[str]):
    logger.info("Starting cleanup process...")
    for path in file_paths:
        if not os.path.exists(path):
            logger.info(f"File {path} not found. Skipping.")
            continue

        try:
            os.remove(path)
            logger.info(f"File {path} has been successfully removed.")
        except PermissionError as e:
            raise click.ClickException(
                f"Permission denied while trying to remove {path}: {e}"
            )
        except Exception as e:
            raise click.ClickException(f"Error removing file {path}: {e}")
