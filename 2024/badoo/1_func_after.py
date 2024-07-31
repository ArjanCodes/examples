from pathlib import Path


def load_data(file_path: Path) -> str:
    with open(file_path, "r") as file:
        return file.read()


def main() -> None:
    data = load_data(Path("data.txt"))
    print(data)


if __name__ == "__main__":
    main()
