def read_and_sum_integers(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            total = 0
            for line in file:
                try:
                    num = int(line.strip())
                    total += num
                except ValueError as e:
                    raise ValueError(
                        f"Invalid content in file: '{line.strip()}'"
                    ) from e
            return total
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except OSError as e:
        raise RuntimeError(f"An unexpected OS error occurred: {e}") from e


def main():
    file_path = "numbers.txt"

    try:
        total = read_and_sum_integers(file_path)
        print(f"Sum of integers: {total}")
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
