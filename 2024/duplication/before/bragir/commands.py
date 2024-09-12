import os

import click

from bragir.directory import get_files_in_directory
from bragir.file import (
    chunk_content,
    chunk_content_into_srt_parts,
    get_new_file_path,
    process_files,
)
from bragir.files.file import File
from bragir.files.operations import create_file, read_file
from bragir.languages import Languages, parse_languages
from bragir.messages import PROMPT_HELP
from bragir.path import get_target_path
from bragir.srt.srt_part import SRTPart
from bragir.time import update_timestamps
from bragir.transcription import transcribe_file
from bragir.translation import translate_srt


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
@click.pass_context
def transcribe(context: click.Context, path: str, output: str) -> None:
    """
    The transcribe command generates an SRT file based on an .mp4 or .mp3 file.
    If output is not set, then it will take the file_path name and change the extension.
    """
    click.echo("Starting transcription")

    path_is_file = os.path.isfile(path)
    path_is_directory = os.path.isdir(path)

    if not path_is_file and not path_is_directory:
        click.echo("Please provide a file or directory")
        exit(1)

    transcriber = context.obj["client"]

    file_paths: list[str] = []

    if path_is_directory:
        directory_file_paths = get_files_in_directory(path)
        file_paths = [*file_paths, *directory_file_paths]

    if path_is_file:
        file_paths.append(path)

    click.echo(f"Starting transcription of {path}")

    for file_path in file_paths:
        transcripts: list[str] = transcribe_file(transcriber, file_path)

        videos_srts: list[tuple[int, list[SRTPart]]] = [
            (order, chunk_content_into_srt_parts(transcript))
            for order, transcript in enumerate(transcripts)
        ]

        sorted_videos = sorted(videos_srts)

        srt_parts: list[SRTPart] = update_timestamps(sorted_videos)

        contents = "".join([srt_part.srt_format for srt_part in srt_parts])

        target_path = get_target_path(file_path, output)

        with open(target_path, "w", encoding="utf-8") as fileIO:
            fileIO.write(contents)
            click.echo(f"Created {target_path} for video {path}")
            click.echo(f"Created {target_path} for video {path}")


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
def translate(context: click.Context, path: str, language: str) -> None:
    """
    The translate command, translates either a single SRT file or files or directory of SRT files into the wanted language.
    """
    click.echo("Starting translation")

    translator = context.obj["client"]

    path_is_file = os.path.isfile(path)
    path_is_directory = os.path.isdir(path)

    if not path_is_directory and not path_is_file:
        click.echo("Please provide a file or directory")
        exit(1)

    translate_to_languages: list[Languages] = parse_languages(language)

    click.echo(
        f"Translating to following language/languages: {' '.join([language.value for language in translate_to_languages])}"
    )

    files: list[File] = []
    if path_is_file:
        click.echo(f"Adding file {path} for translation")

        for target_language in translate_to_languages:
            click.echo(
                f"Adding file {path} with {target_language.value} for translation"
            )

            target_path = get_new_file_path(path, target_language)

            file_content = read_file(path)

            (srt_parts, breakpoints) = chunk_content(file_content)

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

    if path_is_directory:
        directory_file_paths = get_files_in_directory(path)

        num_of_file_paths = len(directory_file_paths)

        if num_of_file_paths == 1:
            click.echo(f"Processing {num_of_file_paths} file in directory {path}")
        else:
            click.echo(f"Processing {num_of_file_paths} files in directory {path}")

        files = process_files(directory_file_paths, translate_to_languages)

    num_of_file_paths = len(files)

    if num_of_file_paths == 1:
        click.echo(f"Processing {num_of_file_paths} file")
    else:
        click.echo(f"Processing {num_of_file_paths} files")

    for target_file in files:
        translated_content = translate_srt(
            translator, target_file, target_file.language.value
        )
        create_file(target_file, translated_content)

        click.echo(f"Created file {target_file.target_path}")
