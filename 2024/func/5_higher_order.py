from functools import partial
from typing import Callable


def bubble_sort(data: list[int]) -> list[int]:
    sorted_data = data.copy()  # copy the data to ensure immutability
    n = len(sorted_data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if sorted_data[j] > sorted_data[j + 1]:
                sorted_data[j], sorted_data[j + 1] = sorted_data[j + 1], sorted_data[j]
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


def multiply_by_n(data: list[int], n: int) -> list[int]:
    return [item * n for item in data]


def add_n(data: list[int], n: int) -> list[int]:
    return [item + n for item in data]


def do_operations(
    data: list[int], sort_fn: Callable[[list[int]], list[int]]
) -> list[int]:
    # multiply each element by 2
    multiply_by_2 = partial(multiply_by_n, n=2)
    data = multiply_by_2(data)

    # add 10 to each element
    add_10 = partial(add_n, n=10)
    data = add_10(data)

    return sort_fn(data)


def main() -> None:
    data = [1, 5, 3, 4, 2]
    print(f"Data before sorting: {data}")

    result = do_operations(data, bubble_sort)
    print(f"Result after bubble sort: {result}")

    result = do_operations([1, 5, 3, 4, 2], quick_sort)
    print(f"Result after quick sort: {result}")


if __name__ == "__main__":
    main()
