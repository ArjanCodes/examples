import os
from typing import Callable

import click

from bragir.audio.chunking import chunk_audio
from bragir.files import File
from bragir.languages import Languages
from bragir.srt.srt_part import SRTPart, get_number_of_tokens
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


def get_srt_parts(content: str) -> list[SRTPart]:
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


def group_parts(
    values: list[SRTPart],
    limit: int | float,
    token_counter: Callable[[str], int] = get_number_of_tokens,
) -> list[list[SRTPart]]:
    grouped_chunks: list[list[SRTPart]] = []
    buffer: int = 0
    pointer_a: int = 0
    pointer_b: int = 0

    if len(values) == 0:
        return []

    if len(values) == 1:
        return [values]

    for value in values:
        raw_value = value.content

        tokens = token_counter(raw_value)
        buffer += tokens

        if buffer >= limit:
            grouped_chunks.append(values[pointer_a:pointer_b])
            pointer_a = pointer_b
            buffer = 0

        # If we are at the end of the list
        if pointer_b == len(values) - 1:
            grouped_chunks.append(values[pointer_a : pointer_b + 1])
            break

        pointer_b += 1

    return grouped_chunks


def group_values(
    values: list[str],
    limit: int,
    token_counter: Callable[[str], int] = get_number_of_tokens,
) -> list[list[str]]:
    grouped_chunks: list[list[str]] = []
    buffer: int = 0
    pointer_a: int = 0
    pointer_b: int = 0

    if len(values) == 0:
        return []

    if len(values) == 1:
        return [values]

    for value in values:
        tokens = token_counter(value)
        buffer += tokens

        if buffer >= limit:
            grouped_chunks.append(values[pointer_a:pointer_b])
            pointer_a = pointer_b
            buffer = 0

        # If we are at the end of the list
        if pointer_b == len(values) - 1:
            grouped_chunks.append(values[pointer_a : pointer_b + 1])
            break

        pointer_b += 1

    return grouped_chunks


def process_file(file_path: str) -> list[str]:
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower().replace(".", "")

    chunks = chunk_audio(file_path=file_path, format=file_extension)
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
