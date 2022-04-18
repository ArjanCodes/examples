from functools import partial
from typing import Callable


def greet(name: str, greeting_type: str) -> str:
    return greeting_type + ", " + name


def greet_list(names: list[str], greet_fn: Callable[[str], str]) -> list[str]:
    return [greet_fn(name) for name in names]


def read_name() -> str:
    return input("Enter your name: ")


def main():
    greet_hello = partial(greet, greeting_type="Hello")
    print(greet_hello(read_name()))
    print("\n".join(greet_list(["John", "Jane", "Joe"], greet_hello)))


if __name__ == "__main__":
    main()
