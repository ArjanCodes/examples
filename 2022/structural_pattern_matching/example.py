"""
Example application showing Python 3.10 structural pattern matching.
"""

import shlex
from dataclasses import dataclass
from typing import List


def run_command_v1(command: str) -> None:
    match command:
        case "quit":
            print("Quitting the program.")
        case "reset":
            print("Resetting the system.")
        case other:
            print(f"Unknown command '{other}'.")


def run_command_v2(command: str) -> None:
    match command.split():
        case ["load", filename]:
            print(f"Loading filename {filename}.")
        case ["save", filename]:
            print(f"Saving filename {filename}.")
        case ["quit" | "exit" | "bye", *rest]:
            if "--force" in rest or "-f" in rest:
                print("Sending SIGTERM to all processes and quitting the program.")
            else:
                print("Quitting the program.")
            quit()
        case _:
            print(f"Unknown command '{command}'.")


def run_command_v3(command: str) -> None:
    match command.split():
        case ["load", filename]:
            print(f"Loading filename {filename}.")
        case ["save", filename]:
            print(f"Saving filename {filename}.")
        case ["quit" | "exit" | "bye", *rest] if "--force" in rest or "-f" in rest:
            print("Sending SIGTERM to all processes and quitting the program.")
            quit()
        case ["quit" | "exit" | "bye"]:
            print("Quitting the program.")
            quit()
        case _:
            print(f"Unknown command {command!r}.")


@dataclass
class Command:
    """Class that represents a command."""

    command: str
    arguments: List[str]


def run_command_v4(command: Command) -> None:
    match command:
        case Command(command="load", arguments=[filename]):
            print(f"Loading filename {filename}.")
        case Command(command="save", arguments=[filename]):
            print(f"Saving filename {filename}.")
        case Command(
            command="quit" | "exit" | "bye", arguments=["--force" | "-f", *rest]
        ):
            print("Sending SIGTERM to all processes and quitting the program.")
            quit()
        case Command(command="quit" | "exit" | "bye"):
            print("Quitting the program.")
            quit()
        case _:
            print(f"Unknown command {command!r}.")


def main() -> None:
    """Main function."""

    while True:
        # command = input("$ ")
        # run_command_v3(command)
        # read a command with arguments from the input
        command, *arguments = shlex.split(input("$ "))

        # run the command
        run_command_v4(Command(command, arguments))


if __name__ == "__main__":
    main()
