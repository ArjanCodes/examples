from functools import partial, reduce
from typing import Callable, Iterator


def multiply_by_x(data: Iterator[int], x: int) -> Iterator[int]:
    for item in data:
        yield item * x


def add_x(data: Iterator[int], x: int) -> Iterator[int]:
    for item in data:
        yield item + x


type Composable[T] = Callable[[T], T]


def compose[T](*functions: Composable[T]) -> Composable[T]:
    def apply(value: T, fn: Composable[T]) -> T:
        return fn(value)

    return lambda data: reduce(apply, functions, data)


def main() -> None:
    # Compose the lazy operations
    multiply_by_2 = partial(multiply_by_x, x=2)
    add_10 = partial(add_x, x=10)
    composed_operations = compose(multiply_by_2, add_10)

    # Original data
    data = [1, 5, 3, 4, 2]

    # Now go through part of the data
    transformed_data = composed_operations(iter(data))
    for _ in range(3):
        print(next(transformed_data))


if __name__ == "__main__":
    main()
