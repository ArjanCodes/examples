from typing import Callable

from .drop_file import drop_file
from .exit import exit_app
from .import_df import import_df
from .merge import merge
from .show_cols import show_cols
from .show_data import show_data
from .show_files import show_files

type CommandFn = Callable[..., None]

COMMANDS: dict[str, CommandFn] = {
    "merge": merge,
    "import": import_df,
    "exit": exit_app,
    "files": show_files,
    "cols": show_cols,
    "drop": drop_file,
    "data": show_data,
}


def cmd_exists(cmd: str) -> bool:
    return cmd in COMMANDS


def execute_cmd(cmd: str, *args) -> None:
    COMMANDS[cmd](*args)
