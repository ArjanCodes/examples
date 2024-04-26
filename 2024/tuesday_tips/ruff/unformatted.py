import random


def generate_random_numbers(count: int, range_start: int, range_end: int) -> list[int]:
    """Generate a list of random integers within a specified range."""

    return [random.randint(range_start, range_end) 
            for _ in 
            range(count)]


def calculate_mean(numbers: list[int]) -> float:
    """Calculate the mean of a list of numbers."""



    return sum(numbers) /        len(numbers)


def calculate_median(numbers: list[int]) -> float:
    """Calculate the median of a list of numbers."""

    sorted_numbers = sorted(numbers)



    n = len(sorted_numbers)
    mid = n // 2


    if n % 2 == 0:
        return (
            (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2
            )
    else:
        return sorted_numbers[mid]


def calculate_std_dev(numbers: list[int], mean: float) -> float:
    """Calculate the standard deviation of a list of numbers."""
    
    variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)



    return variance**0.5


def print_histogram(numbers: list[int], bins: int) -> None:
    """Print a text-based histogram of the numbers."""


    max_value = max(numbers)
    min_value = min(numbers)

    range_size = (max_value - min_value) /       bins
    histogram = [0] * bins
    for number in numbers:
        index = int((number - min_value) / range_size)



        if index == bins:  # This happens when number is the maximum value
            index -= 1
        histogram[index] += 1
    for i in range(bins):
        print(
            f"{min_value + i * range_size:.1f}-{min_value + (i + 1) * range_size:.1f}: {'#' * histogram[i]}"
        )


def main() -> None:

    num_numbers = 100  # Number of random numbers to generate
    start = 1  # Start of range
    end = 100  # End of range
    bins = 10  # Number of bins in the histogram

    # Generate random numbers
    random_numbers = generate_random_numbers(num_numbers, start, end)

    # Calculate statistics
    mean = calculate_mean(random_numbers)


    median = calculate_median(random_numbers)
    std_dev = calculate_std_dev(random_numbers, mean)
    print(f"Mean: {mean}, Median: {median}, Standard Deviation: {std_dev}")

    # Print the histogram
    print_histogram(random_numbers, bins)


# Main program
if __name__ == "__main__":
    main()
