from __future__ import annotations

from dataclasses import dataclass
from typing import IO, Optional


@dataclass
class FileResource:
    path: str
    mode: str = "r"
    file: Optional[IO[str]] = None

    def __enter__(self) -> FileResource:
        print(f"Opening {self.path}")
        self.file = open(self.path, self.mode, encoding="utf-8")
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        print(f"Closing {self.path}")
        if self.file is not None:
            self.file.close()


with FileResource("example.txt", "w") as res:
    assert res.file is not None
    res.file.write("Hello world!")
    print(res.path, res.mode)
