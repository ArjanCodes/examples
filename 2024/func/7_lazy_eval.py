from functools import partial, reduce
from typing import Callable, Iterator


# Lazy evaluation function: Multiply each element by n
def multiply_by_n(data: Iterator[int], n: int) -> Iterator[int]:
    for item in data:
        yield item * n


# Lazy evaluation function: Add n to each element
def add_n(data: Iterator[int], n: int) -> Iterator[int]:
    for item in data:
        yield item + n


# Function to compose other functions
def compose[T](*functions: Callable[[T], T]) -> Callable[[T], T]:
    return lambda data: reduce(lambda acc, fn: fn(acc), functions, data)


def main() -> None:
    # Compose the lazy operations
    multiply_by_2 = partial(multiply_by_n, n=2)
    add_10 = partial(add_n, n=10)
    composed_operations = compose(multiply_by_2, add_10)

    # Original data
    data = [1, 5, 3, 4, 2]

    # Now go through part of the data
    transformed_data = composed_operations(iter(data))
    for _ in range(3):
        print(next(transformed_data))


if __name__ == "__main__":
    main()
