from datetime import datetime
import json
from pathlib import Path
import re
import click
import glob
import os
from file import create_files


@click.command()
@click.argument("pattern")
@click.option("--start", default=0, help="Start index for the notes")
@click.option("--end", default=10, help="End index for the notes")
@click.option("--content", help="Content of the notes", default="")
@click.option("--tags", help="Comma-separated list of tags", default="")
@click.pass_context
def create(
    ctx: click.Context, pattern: str, start: int, end: int, content: str, tags: str
):
    """Create multiple notes with a pattern."""
    notes_directory = ctx.obj["notes_directory"]

    files = create_files(pattern=pattern, start=start, end=end)

    for file_path in files:
        file_name = Path(file_path).stem

        note_name = f"{file_name}.txt"

        note_data: dict[str, str | list[str] | datetime] = {
            "content": content,
            "tags": tags.split(",") if tags else [],
            "created_at": datetime.now().isoformat(),
        }
        with open(notes_directory / note_name, "w") as file:
            json.dump(note_data, file)
        click.echo(f"Note '{file_name}' created.")


@click.command()
@click.argument("pattern")
@click.pass_context
def delete(ctx: click.Context, pattern: str):
    """Delete notes that follows a pattern."""
    notes_directory = ctx.obj["notes_directory"]
    files = glob.glob(pattern)

    for file_path in files:
        file_name = Path(file_path).stem
        note_name = f"{file_name}.txt"
        if not (notes_directory / note_name).exists():
            click.echo(f"Note with title '{file_name}' does not exist. Skipping.")
            continue

        (notes_directory / note_name).unlink()
        click.echo(f"Note '{file_name}' deleted.")


@click.command()
@click.argument("pattern")
@click.option("--content", help="New content of the notes")
@click.pass_context
def update(ctx: click.Context, pattern: str, content: str):
    """Update notes that follows a pattern."""
    notes_directory = ctx.obj["notes_directory"]
    files = glob.glob(pattern)

    for file_path in files:
        file_name = Path(file_path).stem
        note_name = f"{file_name}.txt"

        note_data = json.loads((notes_directory / note_name).read_text())
        note_data["content"] = content
        note_data["updated_at"] = datetime.now().isoformat()

        with open(notes_directory / note_name, "w") as file:
            json.dump(note_data, file)
        click.echo(f"Note '{file_name}' updated.")


def to_snake_case(s: str):
    s = re.sub(r"(?<!^)(?=[A-Z])", "_", s)
    s = s.replace("-", "_")
    return s.lower()


def to_kebab_case(s: str):
    s = re.sub(r"(?<!^)(?=[A-Z])", "-", s)
    s = s.replace("_", "-")
    return s.lower()


def to_camel_case(s: str):
    words = re.split("_|-", s)
    return words[0].lower() + "".join(word.title() for word in words[1:])


def to_pascal_case(s: str):
    return to_camel_case(s).title()


NAMING_CONVENTIONS = {
    "snake_case": to_snake_case,
    "kebab_case": to_kebab_case,
    "camel_case": to_camel_case,
    "pascal_case": to_pascal_case,
}


@click.command()
@click.argument("from_pattern")
@click.argument(
    "naming_convention",
    type=click.Choice(list(NAMING_CONVENTIONS.keys())),
    default="snake_case",
)
@click.pass_context
def rename(ctx: click.Context, from_pattern: str, naming_convention: str):
    """Rename notes to a naming convention."""
    notes_directory = ctx.obj["notes_directory"]

    path = os.path.join(notes_directory, from_pattern)
    files = glob.glob(path)

    print(files)
    for file_path in files:
        file_name = Path(file_path).stem
        note_name = f"{file_name}.txt"

        naming_convetion_func = NAMING_CONVENTIONS[naming_convention]

        new_name = naming_convetion_func(file_name) + ".txt"

        os.rename(notes_directory / note_name, notes_directory / new_name)
        click.echo(f"Note '{file_name}' renamed to '{new_name}'.")
