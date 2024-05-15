import random
from typing import Callable, List, Union

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


# Pure function with immutability and pattern matching
def quick_sort(data: List[int]) -> List[int]:
    match data:
        case []:
            return []
        case [x]:
            return [x]
        case _:
            pivot = data[-1]
            greater: List[int] = [item for item in data[:-1] if item > pivot]
            lesser: List[int] = [item for item in data[:-1] if item <= pivot]
            return quick_sort(lesser) + [pivot] + quick_sort(greater)


# Pure function: Multiply each element by 2
def multiply_by_2(data: List[int]) -> List[int]:
    return [item * 2 for item in data]


# Pure function: Add a random number to each element
def add_random(data: List[int]) -> List[int]:
    return [item + random.randint(-10, 10) for item in data]


# Function to demonstrate operations with pattern matching
def do_operations_with_pattern_matching(data: List[int], sort_fn: SortFn) -> List[int]:
    transformed_data: Union[List[int], None] = None

    # Pattern matching on operations
    match data:
        case []:
            transformed_data = []
        case [x]:
            transformed_data = [x * 2 + random.randint(-10, 10)]
        case [x, y]:
            transformed_data = [
                x * 2 + random.randint(-10, 10),
                y * 2 + random.randint(-10, 10),
            ]
        case _:
            transformed_data = add_random(multiply_by_2(data))

    print(f"Data before sorting (pattern matching): {transformed_data}")
    result = sort_fn(transformed_data)
    print(f"Result after sorting (pattern matching): {result}")

    return result


def main() -> None:
    # Original data
    data = [1, 5, 3, 4, 2]

    # Using pattern matching with bubble sort
    print("Using pattern matching with Bubble Sort:")
    do_operations_with_pattern_matching(data, bubble_sort)

    # Using pattern matching with quick sort
    print("\nUsing pattern matching with Quick Sort:")
    do_operations_with_pattern_matching(data, quick_sort)

    # Ensure the original data is unchanged
    print(f"\nOriginal data after operations: {data}")


if __name__ == "__main__":
    main()
