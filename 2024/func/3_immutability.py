def bubble_sort(data: list[int]) -> list[int]:
    print(f"Data before sorting: {data}")
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


def do_operations(data: list[int]) -> None:
    transformed_data = [item * 2 + 10 for item in data]
    result = bubble_sort(transformed_data)

    print(f"Result after sorting: {result}")


def main() -> None:
    data = [1, 5, 3, 4, 2]
    do_operations(data)


if __name__ == "__main__":
    main()
