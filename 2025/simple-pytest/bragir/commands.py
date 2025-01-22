import asyncio
from pathlib import Path

import click
from openai import AsyncOpenAI

from bragir.config import (
    CONFIG_FILE_PATH,
    Config,
    create_config_file,
    get_config,
    read_config,
    reset_config_file,
    set_config,
    update_dict,
)
from bragir.constants.ai import POSSIBLE_MODELS, get_model_limit
from bragir.file import (
    get_new_file_path,
    get_srt_parts,
    read_file,
)
from bragir.files import create_file
from bragir.languages import Languages, parse_languages
from bragir.messages import PROMPT_HELP
from bragir.path import get_files, get_target_path
from bragir.post_processing import process_text
from bragir.spinner import spinner
from bragir.srt.srt_part import SRTPart
from timestamp_utils import update_timestamps
from bragir.tracing.logger import logger
from bragir.transcription import async_transcribe_file
from bragir.translation import async_translate_srt_parts


@click.command(options_metavar="<options>")
@click.argument(
    "path",
    type=click.Path(exists=True, file_okay=True, dir_okay=True),
    metavar="<path>",
)
@click.argument(
    "output",
    type=click.Path(exists=False, file_okay=True, dir_okay=True, writable=True),
    required=False,
)
@spinner("transcribe")
@click.pass_context
def transcribe(context: click.Context, path: str, output: str) -> None:
    """
    The transcribe command generates an SRT file based on an .mp4 or .mp3 file.
    If output is not set, then it will take the file_path name and change the extension.
    """
    logger.info("Starting transcription")

    transcriber: AsyncOpenAI = context.obj["client"]

    file_paths = get_files(path)

    for file_path in file_paths:
        transcripts = asyncio.run(
            async_transcribe_file(transcriber=transcriber, path=file_path)
        )

        print(transcripts)

        videos_srts: list[tuple[int, list[SRTPart]]] = [
            (order, get_srt_parts(transcript))
            for order, transcript in enumerate(transcripts)
        ]

        sorted_videos = sorted(videos_srts)

        srt_parts: list[SRTPart] = update_timestamps(sorted_videos)

        contents = "".join([srt_part.raw_srt_format for srt_part in srt_parts])

        target_path = get_target_path(file_path, output)

        with open(target_path, "w", encoding="utf-8") as fileIO:
            logger.info(f"Creating {target_path} for video {path}")
            fileIO.write(contents)


@click.command(options_metavar="<options>")
@click.argument(
    "path",
    type=click.Path(dir_okay=True, exists=True),
    metavar="<path>",
)
@click.option(
    "--language",
    "-l",
    required=True,
    type=click.Choice([language.value for language in Languages], case_sensitive=False),
    multiple=True,
    help=PROMPT_HELP["language"],
)
@click.pass_context
@spinner("translate")
def translate(context: click.Context, path: str, language: str) -> None:
    """
    The translate command, translates either a single SRT file or files or directory of SRT files into the wanted language.
    """
    translator: AsyncOpenAI = context.obj["client"]

    config = get_config()

    if config is None:
        logger.error("Config file not found")
        exit(1)

    logger.info("Config file found")

    limit = get_model_limit(config.client.model)

    if limit is None:
        logger.error("Model limit not found")
        exit(1)

    logger.info(f"Model limit: {limit}")

    file_paths = get_files(path)
    num_of_file_paths = len(file_paths)

    if num_of_file_paths == 1:
        logger.info(f"Translating {file_paths[0]}")
    else:
        logger.info(f"Translating {num_of_file_paths} files in directory {path}")

    translate_to_languages: list[Languages] = parse_languages(language)
    logger.info(
        f"Translating to following language/languages: {' '.join([language.value for language in translate_to_languages])}"
    )

    for file_path in file_paths:
        file_content = read_file(file_path)

        srt_parts: list[SRTPart] = get_srt_parts(file_content)

        translated_parts = asyncio.run(
            async_translate_srt_parts(
                translator=translator, srt_parts=srt_parts, language=language
            )
        )

        for translated_part in translated_parts:
            translated_part.translation = process_text(translated_part.translation)

        translation: str = ""

        for traslated_part in translated_parts:
            translation += traslated_part.translated_raw_srt_format

        for language in translate_to_languages:
            new_file_path = get_new_file_path(file_path, language)
            create_file(new_file_path, translation)
            logger.info(f"Created file {new_file_path}")


@click.group(invoke_without_command=False)
def config() -> None:
    pass


@config.command()
@click.option(
    "--path",
    "-p",
    required=False,
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
    help="Path to the config file",
)
def create(path: Path | None) -> None:
    """
    Creates a new config file.
    """

    target_path = Path(path) if path else Path(CONFIG_FILE_PATH)

    if target_path.exists():
        logger.info(f"Config file already exists at {target_path}")
        exit(1)

    create_config_file(file_path=target_path)


@config.command()
@click.option(
    "--path",
    "-p",
    required=False,
    type=click.Path(exists=True, file_okay=True, dir_okay=True),
    default=CONFIG_FILE_PATH,
    help="Path to the config file",
)
def show(path: Path) -> None:
    """
    Displays the current config file.
    """

    target_path = Path(path) if path else Path(CONFIG_FILE_PATH)

    logger.info(f"Reading config file at {target_path}")
    read_config(file_path=target_path)


@config.command()
@click.option(
    "--path",
    "-p",
    required=False,
    type=click.Path(exists=True, file_okay=True, dir_okay=True),
    default=CONFIG_FILE_PATH,
    help="Path to the config file",
)
def reset(path: Path) -> None:
    """
    Resets the current config file to default.
    """

    target_path = Path(path) if path else Path(CONFIG_FILE_PATH)

    reset_config_file(target_path=target_path)


@config.command()
@click.option(
    "--path",
    "-p",
    required=False,
    type=click.Path(exists=True, file_okay=True, dir_okay=True),
    default=CONFIG_FILE_PATH,
)
@click.option(
    "--model",
    "-m",
    required=False,
    type=click.Choice(POSSIBLE_MODELS, case_sensitive=False),
    help="OpenAI model",
)
@click.option(
    "--min_silence_len",
    "-msl",
    required=False,
    type=click.IntRange(0, 10000),
    help="Minimum silence length in milliseconds",
)
@click.option(
    "--silence_thresh",
    "-st",
    required=False,
    type=click.IntRange(-100, 0),
    help="Silence threshold in dB",
)
@click.option(
    "--keep_silence",
    "-ks",
    required=False,
    type=click.BOOL,
    help="Keep silence",
    default=False,
)
def update(path: Path, **kwargs: dict[str, str | int | bool | None] | None) -> None:
    """
    Updates the config file with the given values of the options.
    """

    target_path = Path(path) if path else Path(CONFIG_FILE_PATH)

    config = get_config(file_path=target_path)

    if config is None:
        logger.error("Config file not found")
        exit(1)

    updates = {key: value for key, value in kwargs.items() if value is not None}

    updated_dict = update_dict(config.model_dump(), updates)

    updated_config = Config(**updated_dict)

    set_config(file_path=target_path, config=updated_config)

    for key, value in updates.items():
        logger.info(f"Updated {key} to {value}")
