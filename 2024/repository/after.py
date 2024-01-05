import contextlib
import sqlite3
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class Post:
    title: str
    content: str
    id: Optional[int] = None


class Repository[T](ABC):
    @abstractmethod
    def get(self, id: int) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def add(self, **kwargs: object) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, id: int, **kwargs: object) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: int) -> None:
        raise NotImplementedError


class PostRepository(Repository[Post]):
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.create_table()

    @contextlib.contextmanager
    def connect(self):
        with sqlite3.connect(self.db_path) as conn:
            yield conn.cursor()

    def create_table(self) -> None:
        with self.connect() as cursor:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, title TEXT, content TEXT)"
            )

    def get(self, id: int) -> Post:
        with self.connect() as cursor:
            cursor.execute("SELECT * FROM posts WHERE id=?", (id,))
            post = cursor.fetchone()
            if post is None:
                raise ValueError(f"Post with id {id} does not exist")
            return Post(*post)

    def get_all(self) -> list[Post]:
        with self.connect() as cursor:
            cursor.execute("SELECT * FROM posts")
            return [Post(*post) for post in cursor.fetchall()]

    def add(self, **kwargs: object) -> None:
        if "content" in kwargs and "title" in kwargs:
            with self.connect() as cursor:
                cursor.execute(
                    "INSERT INTO posts (title, content) VALUES (?, ?)",
                    (kwargs["title"], kwargs["content"]),
                )
        elif "content" in kwargs:
            with self.connect() as cursor:
                cursor.execute(
                    "INSERT INTO posts (content) VALUES (?)", (kwargs["content"],)
                )
        elif "title" in kwargs:
            with self.connect() as cursor:
                cursor.execute(
                    "INSERT INTO posts (title) VALUES (?)", (kwargs["title"],)
                )
        else:
            raise ValueError("Must provide either content or title")

    def update(self, id: int, **kwargs: object) -> None:
        if "content" in kwargs and "title" in kwargs:
            with self.connect() as cursor:
                cursor.execute(
                    "UPDATE posts SET title=?, content=? WHERE id=?",
                    (kwargs["title"], kwargs["content"], id),
                )
        elif "content" in kwargs:
            with self.connect() as cursor:
                cursor.execute(
                    "UPDATE posts SET content=? WHERE id=?", (kwargs["content"], id)
                )
        elif "title" in kwargs:
            with self.connect() as cursor:
                cursor.execute(
                    "UPDATE posts SET title=? WHERE id=?", (kwargs["title"], id)
                )
        else:
            raise ValueError("Must provide either content or title")

    def delete(self, id: int) -> None:
        with self.connect() as cursor:
            cursor.execute("DELETE FROM posts WHERE id=?", (id,))


def main() -> None:
    repo = PostRepository("posts.db")
    repo.add(title="Hello", content="World")
    repo.add(title="Foo", content="Bar")
    print(repo.get_all())
    repo.update(0, title="Hello World")
    print(repo.get_all())
    repo.delete(1)
    print(repo.get_all())


if __name__ == "__main__":
    main()
