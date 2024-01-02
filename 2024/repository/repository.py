from contextlib import contextmanager
from sqlite3 import connect, Cursor
from typing import Generator, Protocol


class Repository[RepoObject](Protocol):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.create_table()

    @contextmanager
    def connect(self) -> Generator[Cursor, None, None]:
        with connect(self.db_path) as conn:
            yield conn.cursor()

    def get(self, id: int) -> RepoObject:
        ...

    def get_all(self) -> list[RepoObject]:
        ...

    def add(self, **kwargs: object) -> None:
        raise NotImplementedError

    def update(self, id: int, **kwargs: object) -> None:
        raise NotImplementedError

    def delete(self, id: int) -> None:
        raise NotImplementedError

    def create_table(self) -> None:
        raise NotImplementedError
