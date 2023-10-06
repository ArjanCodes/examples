from __future__ import annotations
from typing import Any, Generic, Optional, TypeVar, Callable

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
def safe_divide(x: float, y: float) -> Maybe[float]:
    return Maybe(None) if y == 0 else Maybe(x / y)


def process_result(maybe_result: Maybe[float]) -> str:
    match maybe_result:
        case Maybe(None):
            return "Cannot divide by zero!"
        case Maybe(value=float()):
            return f"Result: {maybe_result.value}"
        case _:
            return "Unexpected input!"


def main() -> None:
    x, y = 10.0, 0
    result = (
        Maybe.unit(x)
        .bind(lambda x: safe_divide(x, 2))
        .bind(lambda x: safe_divide(x, y))
    )

    print(process_result(result))  # Output: Cannot divide by zero!


if __name__ == "__main__":
    main()
