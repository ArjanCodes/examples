from pathlib import Path
import click
from config import CONFIG_FILE, DEFAULT_NOTES_DIR, load_config, save_config
import crud
import bulk_crud


@click.group()
@click.version_option()
@click.pass_context
def cli(ctx: click.Context):
    """A simple note-taking application."""
    config = load_config()

    notes_directory = config.get("notes_directory", DEFAULT_NOTES_DIR)

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
def create():
    """Create a new configuration."""
    config = load_config()
    save_config(config)
    click.echo("Configuration created.")


@config.command()
def show():
    """Show the current configuration."""
    if not CONFIG_FILE.exists():
        click.echo("No configuration found.")
        return

    config = load_config()
    click.echo(f"Notes directory: {config.get('notes_directory', DEFAULT_NOTES_DIR)}")


@config.command()
@click.option("--notes_directory", "-n", type=click.Path(exists=True))
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
