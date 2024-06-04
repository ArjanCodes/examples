from functools import partial, reduce
from typing import Callable


def multiply_by_n(data: list[int], n: int) -> list[int]:
    return [item * n for item in data]


def add_n(data: list[int], n: int) -> list[int]:
    return [item + n for item in data]


type Composable[T] = Callable[[T], T]


def compose[T](*functions: Composable[T]) -> Composable[T]:
    def apply(value: T, fn: Composable[T]) -> T:
        return fn(value)

    return lambda data: reduce(apply, functions, data)


def bubble_sort(data: list[int]) -> list[int]:
    sorted_data = data.copy()  # copy the data to ensure immutability
    n = len(sorted_data)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if sorted_data[j] > sorted_data[j + 1]:
                sorted_data[j], sorted_data[j + 1] = sorted_data[j + 1], sorted_data[j]
                swapped = True
        if not swapped:
            break
    return sorted_data


def quick_sort(data: list[int]) -> list[int]:
    match data:
        case []:
            return []
        case [x]:
            return [x]
        case _:
            pivot = data[-1]
            greater = [item for item in data[:-1] if item > pivot]
            lesser = [item for item in data[:-1] if item <= pivot]
            return quick_sort(lesser) + [pivot] + quick_sort(greater)


def main() -> None:
    data = [1, 5, 3, 4, 2]
    print(f"Data before sorting: {data}")

    multiply_by_2 = partial(multiply_by_n, n=2)
    add_10 = partial(add_n, n=10)
    do_operations = compose(multiply_by_2, add_10, quick_sort)

    result = do_operations(data)
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
