from returns.io import IO


def read_file(file_path: str) -> IO[str]:
    with open(file_path, "r") as file:
        return IO(file.read())


def process_data(data: str) -> str:
    # Just a simple transformation for the example
    return data.upper()


def main() -> None:
    file_io = read_file("user_data.txt")
    print(file_io)

    # do something with the data in the IO container
    processed_data = file_io.map(process_data)
    processed_data.map(lambda data: print(data))


if __name__ == "__main__":
    main()
