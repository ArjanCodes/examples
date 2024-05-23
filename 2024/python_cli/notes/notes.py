import os
from pathlib import Path
import click
from config import DEFAULT_NOTES_DIR, load_config, save_config
import crud
import bulk_crud


@click.group()
@click.version_option()
@click.pass_context
def cli(ctx: click.Context):
    """A simple note-taking application."""
    config = load_config()

    notes_directory = config.get("notes_directory", DEFAULT_NOTES_DIR)

    if not os.path.exists(notes_directory):
        os.makedirs(notes_directory)

    ctx.ensure_object(dict)
    ctx.obj["config"] = config
    ctx.obj["notes_directory"] = Path(notes_directory)


@cli.group()
def bulk():
    """Bulk operations on notes."""
    pass


@cli.group()
def config():
    """Configuration options."""
    pass


@config.command()
@click.argument("notes_directory")
def update(notes_dir: str):
    """Setup the notes directory."""
    config = load_config()
    config["notes_directory"] = notes_dir

    save_config(config)
    click.echo(f"Notes directory set to '{notes_dir}'.")


bulk.add_command(bulk_crud.create)
bulk.add_command(bulk_crud.delete)
bulk.add_command(bulk_crud.update)
bulk.add_command(bulk_crud.rename)


cli.add_command(crud.create)
cli.add_command(crud.read)
cli.add_command(crud.update)
cli.add_command(crud.delete)
cli.add_command(crud.show)
