LARGE_STRING = "The quick brown fox jumps over the lazy dog.\n" * 10000

num_iterations = 1000


def write_to_file(text: str) -> None:
    with open("test_file.txt", "w") as file:
        file.write(text)


def read_from_file() -> None:
    with open("test_file.txt", "r") as file:
        file.read()


def main() -> None:
    for _i in range(num_iterations):
        reversed_string = LARGE_STRING[::-1]

        write_to_file(reversed_string)
        read_from_file()


if __name__ == "__main__":
    main()
