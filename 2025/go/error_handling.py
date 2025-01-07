def read_and_sum_integers(file_path):
    try:
        with open(file_path, "r") as file:
            sum = 0
            for line in file:
                try:
                    num = int(line.strip())
                    sum += num
                except ValueError as e:
                    raise ValueError(
                        f"Invalid content in file: '{line.strip()}'"
                    ) from e
            return sum
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}") from e


def main():
    file_path = "numbers.txt"

    try:
        total = read_and_sum_integers(file_path)
        print(f"Sum of integers: {total}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
