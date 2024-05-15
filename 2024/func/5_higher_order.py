from functools import partial
from typing import Callable


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


def multiply_by_x(data: list[int], x: int) -> list[int]:
    return [item * x for item in data]


def add_x(data: list[int], x: int) -> list[int]:
    return [item + x for item in data]


def do_operations(
    data: list[int], sort_fn: Callable[[list[int]], list[int]]
) -> list[int]:
    multiply_by_2 = partial(multiply_by_x, x=2)
    add_10 = partial(add_x, x=10)

    return sort_fn(add_10(multiply_by_2(data)))


def main() -> None:
    data = [1, 5, 3, 4, 2]
    print(f"Data before sorting: {data}")

    result = do_operations(data, bubble_sort)
    print(f"Result after bubble sort: {result}")


if __name__ == "__main__":
    main()
