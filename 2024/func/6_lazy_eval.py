import random
from typing import Callable, Iterator, List

type SortFn = Callable[[List[int]], List[int]]


# Pure function with immutability
def bubble_sort(data: List[int]) -> List[int]:
    sorted_data = data.copy()  # Work with a copy to ensure immutability
    n = len(sorted_data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if sorted_data[j] > sorted_data[j + 1]:
                sorted_data[j], sorted_data[j + 1] = sorted_data[j + 1], sorted_data[j]
    return sorted_data


# Pure function with immutability
def quick_sort(data: List[int]) -> List[int]:
    if len(data) <= 1:
        return data.copy()  # Return a copy to ensure immutability
    else:
        pivot = data[-1]
        greater: List[int] = [item for item in data[:-1] if item > pivot]
        lesser: List[int] = [item for item in data[:-1] if item <= pivot]
        return quick_sort(lesser) + [pivot] + quick_sort(greater)


# Lazy evaluation function: Multiply each element by 2
def multiply_by_2(data: Iterator[int]) -> Iterator[int]:
    for item in data:
        yield item * 2


# Lazy evaluation function: Add a random number to each element
def add_random(data: Iterator[int]) -> Iterator[int]:
    for item in data:
        yield item + random.randint(-10, 10)


# Function to compose lazy evaluation functions
def compose(
    *functions: Callable[[Iterator[int]], Iterator[int]],
) -> Callable[[Iterator[int]], Iterator[int]]:
    def composed_function(data: Iterator[int]) -> Iterator[int]:
        for function in functions:
            data = function(data)
        return data

    return composed_function


def main() -> None:
    # Compose the lazy operations
    composed_operations = compose(multiply_by_2, add_random)

    # Original data
    data = [1, 5, 3, 4, 2]

    # Using composed operations with bubble sort
    print("Using composed operations with Bubble Sort:")
    transformed_data = list(composed_operations(iter(data)))
    print(f"Data before sorting: {transformed_data}")
    print(f"Result after sorting: {bubble_sort(transformed_data)}")

    # Using composed operations with quick sort
    print("\nUsing composed operations with Quick Sort:")
    transformed_data = list(composed_operations(iter(data)))
    print(f"Data before sorting: {transformed_data}")
    print(f"Result after sorting: {quick_sort(transformed_data)}")

    # Ensure the original data is unchanged
    print(f"\nOriginal data after operations: {data}")


if __name__ == "__main__":
    main()
