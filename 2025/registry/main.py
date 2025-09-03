import importlib
import pkgutil

import typer
from registry import get_registry

app = typer.Typer()


def load_text_commands() -> None:
    import commands.text

    for _, module_name, _ in pkgutil.iter_modules(commands.text.__path__):
        importlib.import_module(f"commands.text.{module_name}")


def load_plugins() -> None:
    import plugins

    for _, module_name, _ in pkgutil.iter_modules(plugins.__path__):
        importlib.import_module(f"plugins.{module_name}")


def register_with_typer() -> None:
    group_apps: dict[str, typer.Typer] = {}

    for group, name, func in get_registry():
        if group not in group_apps:
            group_apps[group] = typer.Typer()
            app.add_typer(group_apps[group], name=group)
        group_apps[group].command(name)(func)


def main() -> None:
    load_text_commands()
    load_plugins()
    register_with_typer()
    app()


if __name__ == "__main__":
    main()
