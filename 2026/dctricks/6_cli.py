import argparse
from dataclasses import dataclass, fields
from typing import Self, Type


@dataclass
class CLIArgs:
    @classmethod
    def from_command_line(cls: Type[Self]) -> Self:
        parser = argparse.ArgumentParser()

        for f in fields(cls):
            arg_name = f"--{f.name.replace('_', '-')}"
            if f.type is bool:
                parser.add_argument(arg_name, action="store_true")
            else:
                parser.add_argument(arg_name, type=f.type, default=f.default)

        parsed = parser.parse_args()
        return cls(**vars(parsed))


@dataclass
class Args(CLIArgs):
    verbose: bool = False
    filename: str = "data.txt"
    retries: int = 3


def main() -> None:
    args = Args.from_command_line()
    print(args)


if __name__ == "__main__":
    main()
