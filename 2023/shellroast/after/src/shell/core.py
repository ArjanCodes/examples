from typing import Callable

from colorama import Fore as f

SHELL_HEADER = f"  {f.YELLOW}[*] {f.CYAN}-> {f.WHITE}"

COMMANDS: dict[str, Callable[[list[str]], None]] = {}


def add_command(command: str, function: Callable[[list[str]], None]) -> None:
    COMMANDS[command] = function


def execute(command: str, arguments: list[str]) -> None:
    if command in COMMANDS:
        COMMANDS[command](arguments)


def parse_command_string(command_string: str) -> tuple[str, list[str]]:
    # Split the input string into a list of strings at each space character
    command_parts = command_string.split()

    # If the command is empty, return an empty command and an empty list of arguments
    if not command_parts:
        return "", []

    # Extract the command (the first element in the list) and the arguments (the rest of the list)
    command = command_parts[0].lower().strip()
    arguments = [part.strip() for part in command_parts[1:]]

    return command, arguments


def shell_input() -> tuple[str, list[str]]:
    """Gets User input then returns a parsed command."""
    user_input = input(SHELL_HEADER)
    return parse_command_string(user_input)


def run_shell() -> None:
    while True:
        command, arguments = shell_input()
        execute(command, arguments)
