from typing import Callable

type Greet = Callable[[str], str]


def greet_fn(name: str) -> str:
    return f"Hello, {name}!"
