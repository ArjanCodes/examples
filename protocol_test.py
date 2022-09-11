from dataclasses import dataclass
from typing import Protocol


@dataclass
class What(Protocol):
    something: int

    def some_function(self) -> None:
        pass


class DoesThisWork:
    def some_function(self) -> None:
        print("This works.")


def do_something(what: What):
    print(what.something)


def main():
    do_something(DoesThisWork())


if __name__ == "__main__":
    main()
