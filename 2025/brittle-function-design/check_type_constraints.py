def calculate_average(numbers):
    len_of_numbers = len(numbers)
    if len_of_numbers == 0:
        return 0

    return sum(numbers) / len(numbers)


def calculate_average_1(numbers):
    if not isinstance(numbers, list):
        raise ValueError("Input must be a list.")

    if not all(isinstance(num, (int, float)) for num in numbers):
        raise ValueError("All elements in the list must be integers or floats.")

    len_of_numbers = len(numbers)
    if len_of_numbers == 0:
        return 0

    return sum(numbers) / len(numbers)


def calculate_average_2(numbers: list) -> float:
    if not all(isinstance(num, (int, float)) for num in numbers):
        raise ValueError("All elements in the list must be integers or floats.")

    len_of_numbers = len(numbers)
    if len_of_numbers == 0:
        return 0

    return sum(numbers) / len(numbers)


def calculate_average_3(numbers: list[int | float]) -> float:
    len_of_numbers = len(numbers)
    if len_of_numbers == 0:
        return 0

    return sum(numbers) / len(numbers)
