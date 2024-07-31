from pathlib import Path


class DataLoader:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def load(self) -> str:
        with open(self.file_path, "r") as file:
            return file.read()


def main() -> None:
    loader = DataLoader(Path("data.txt"))
    data = loader.load()
    print(data)


if __name__ == "__main__":
    main()
