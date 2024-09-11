import click

from bragir.directory import get_files
from bragir.file import (
    process_files,
)
from bragir.files.operations import create_file
from bragir.languages import Languages, parse_languages
from bragir.path import get_target_path
from bragir.srt.writer import write_srt_to_file
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

    file_paths = get_files(path)
    transcriber = context.obj["client"]

    for file_path in file_paths:
        transcripts: list[str] = transcribe_file(transcriber, file_path)
        target_path = get_target_path(file_path, output)

        write_srt_to_file(transcripts, target_path)


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
)
@click.pass_context
def translate(context: click.Context, path: str, language: str) -> None:
    """
    The translate command, translates either a single SRT file or files or directory of SRT files into the wanted language.
    """
    click.echo("Starting translation")

    translate_to_languages: list[Languages] = parse_languages(language)

    click.echo(
        f"Translating to following language/languages: {' '.join([language.value for language in translate_to_languages])}"
    )

    file_paths = get_files(path)
    files = process_files(file_paths, translate_to_languages)

    click.echo(f"Processing {len(files)} file(s).")

    translator = context.obj["client"]

    for target_file in files:
        translated_content = translate_srt(
            translator, target_file, target_file.language.value
        )
        create_file(target_file, translated_content)

        click.echo(f"Created file {target_file.target_path}")
