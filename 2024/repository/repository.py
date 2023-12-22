from abc import ABC, abstractmethod
from contextlib import contextmanager
from sqlite3 import connect, Cursor
from typing import Generator


class Repository[RepoObject](ABC):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.create_table()

    @contextmanager
    def connect(self) -> Generator[Cursor, None, None]:
        with connect(self.db_path) as conn:
            yield conn.cursor()

    @abstractmethod
    def get(self, id_: int) -> RepoObject:
        ...

    @abstractmethod
    def get_all(self) -> list[RepoObject]:
        ...

    @abstractmethod
    def add(self, entry: RepoObject) -> None:
        ...

    @abstractmethod
    def update(self, entry: RepoObject) -> None:
        ...

    @abstractmethod
    def delete(self, entry: RepoObject) -> None:
        ...

    @abstractmethod
    def create_table(self) -> None:
        ...
