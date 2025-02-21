def calculate_average(numbers: list[int | float]) -> float:
    """
    Calculates the average of a list of numbers.
    """
    return sum(numbers) / len(numbers)


def main() -> None:
    average = calculate_average([1, 2, 3, 4])

    print(average)


if __name__ == "__main__":
    main()
