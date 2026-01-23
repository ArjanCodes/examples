from dataclasses import dataclass
from typing import IO


@dataclass
class FileResource:
    path: str
    mode: str = "r"
    file: IO[str] | None = None

    def __enter__(self) -> FileResource:
        print(f"Opening {self.path}")
        self.file = open(self.path, self.mode, encoding="utf-8")
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        print(f"Closing {self.path}")
        if self.file is not None:
            self.file.close()


def main() -> None:
    with FileResource("example.txt", "w") as res:
        assert res.file is not None
        res.file.write("Hello world!")
        print(res.path, res.mode)


if __name__ == "__main__":
    main()
