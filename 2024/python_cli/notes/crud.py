from datetime import datetime
import click
import json
import os
from file import load, save, exists


@click.command()
@click.argument("title")
@click.option("--content", prompt=True, help="Content of the note")
@click.option("--tags", help="Comma-separated list of tags")
@click.pass_context
def create(ctx: click.Context, title: str, content: str, tags: str):
    """Create a new note."""
    notes_dir = ctx.obj["notes_dir"]
    note_name = f"{title}.txt"
    if (notes_dir / note_name).exists():
        click.echo(f"Note with title '{title}' already exists.")
        return

    note_data = {
        "content": content,
        "tags": tags.split(",") if tags else [],
        "created_at": datetime.now().isoformat(),
    }
    with open(notes_dir / note_name, "a+") as file:
        json.dump(note_data, file)
    click.echo(f"Note '{title}' created.")


@click.command()
@click.argument("title")
@click.pass_context
def read(ctx: click.Context, title: str):
    """Read the note."""
    notes_dir = ctx.obj["notes_dir"]
    note_name = f"{title}.txt"
    if not (notes_dir / note_name).exists():
        click.echo(f"Note with title '{title}' does not exist.")
        exit(1)

    with open(notes_dir / note_name, "r") as file:
        note_data = json.load(file)
    click.echo(f"Title: {title}")
    click.echo(f"Tags: {', '.join(note_data['tags'])}")
    click.echo(f"Created At: {note_data['created_at']}")
    click.echo(f"Content:\n{note_data['content']}")


@click.command()
@click.argument("title")
@click.option("--content", help="New content of the note")
@click.option("--tags", help="Comma-separated list of new tags")
def update(title: str, content: str, tags: str):
    """Update the note."""
    note_name = f"{title}.txt"
    if not exists(note_name):
        click.echo(f"Note with title '{title}' does not exist.")
        return

    note_data = json.loads(load(note_name))
    if content:
        note_data["content"] = content
    if tags:
        note_data["tags"] = tags.split(",")

    save(note_name, json.dumps(note_data))
    click.echo(f"Note '{title}' updated.")


@click.command()
@click.argument("title")
@click.pass_context
def delete(ctx: click.Context, title: str):
    """Delete the note."""
    notes_dir = ctx.obj["notes_dir"]
    note_name = f"{title}.txt"
    if not (notes_dir / note_name).exists():
        click.echo(f"Note with title '{title}' does not exist.")
        return

    os.remove(notes_dir / note_name)
    click.echo(f"Note '{title}' deleted.")


@click.command()
@click.option("--tag", help="Filter notes by tag")
@click.option("--keyword", help="Search notes by keyword")
@click.pass_context
def show(ctx: click.Context, tag: str, keyword: str):
    """Show notes."""
    notes_dir: str = ctx.obj["notes_dir"]
    notes = [note for note in os.listdir(notes_dir) if note.endswith(".txt")]
    results: list[str] = []

    for note in notes:
        with open(f"{notes_dir}/{note}", "r") as file:
            note_data = json.load(file)
        if tag and tag not in note_data["tags"]:
            continue
        if keyword and keyword not in note_data["content"]:
            continue
        results.append(note.replace(".txt", ""))

    click.echo("Notes:")
    for result in results:
        click.echo(f"- {result}")
