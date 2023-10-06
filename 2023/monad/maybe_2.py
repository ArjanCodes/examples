from __future__ import annotations
from typing import Any, Generic, Optional, Callable, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class Maybe(Generic[T]):
    __match_args__ = ("value",)

    def __init__(self, value: Optional[T]) -> None:
        self.value = value

    def bind(self, func: Callable[[T], Maybe[U]]) -> Maybe[T] | Maybe[U]:
        return self if self.value is None else func(self.value)

    @staticmethod
    def unit(value: T) -> Maybe[T]:
        return Maybe(value)

    def __match__(self, other: Any) -> bool:
        if isinstance(other, Maybe):
            return self.value == other.value
        return False


# Example Usage
def parse_int(s: str) -> Maybe[int]:
    try:
        return Maybe(int(s))
    except ValueError:
        return Maybe(None)


def is_positive(number: int) -> Maybe[int]:
    return Maybe(number) if number > 0 else Maybe(None)


def double(number: int) -> int:
    return 2 * number


# Validate and process user input
def validate_and_process(input_str: str) -> Maybe[str] | Maybe[int]:
    return (
        Maybe.unit(input_str)
        .bind(parse_int)
        .bind(is_positive)
        .bind(lambda n: Maybe(double(n)))
    )


def main() -> None:
    # Example inputs
    inputs = ["5", "-3", "foo"]

    # Process inputs
    for input_str in inputs:
        result = validate_and_process(input_str)
        print(
            f"Processing '{input_str}':",
            "Success" if result.value is not None else "Failure",
        )


if __name__ == "__main__":
    main()
