import os
from pathlib import Path
import click
from config import load_config, DEFAULT_NOTES_DIR, save_config
import crud
import bulk_crud


@click.group()
@click.pass_context
def cli(ctx: click.Context):
    """A simple note-taking application."""
    config = load_config()

    config_path = config.get("notes_dir", DEFAULT_NOTES_DIR)

    if config_path is None:
        click.echo(f"Notes directory '{config_path}' does not exist.")
        click.echo("Please run 'notes setup' to configure the notes directory.")
        exit(1)

    if not os.path.exists(config_path):
        os.makedirs(config_path)

    ctx.ensure_object(dict)
    ctx.obj["config"] = config
    ctx.obj["notes_dir"] = Path(config_path)
    ctx.obj["remote_url"] = config.get("remote_url")


@cli.group()
def bulk():
    """Bulk operations on notes."""
    pass


@cli.group()
def config():
    """Configuration options."""
    pass


@config.command()
@click.argument("notes_dir")
def update(notes_dir: str):
    """Setup the notes directory."""
    config = load_config()
    config["notes_dir"] = notes_dir

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
