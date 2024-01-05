import sqlite3
import contextlib
from dataclasses import dataclass
from typing import Optional


@contextlib.contextmanager
def connect(db_path: str):
    with sqlite3.connect(db_path) as conn:
        yield conn.cursor()


@dataclass
class Post:
    title: str
    content: str
    id: Optional[int] = None

    @classmethod
    def create_table(cls, db_path: str) -> None:
        with connect(db_path) as cursor:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, title TEXT, content TEXT)"
            )

    @classmethod
    def get_post(cls, post_id: int, db_path: str) -> "Post":
        with connect(db_path) as cursor:
            cursor.execute("SELECT * FROM posts WHERE id=?", (post_id,))
            post = cursor.fetchone()
            if post is None:
                raise ValueError(f"Post with id {post_id} does not exist")
            return Post(title=post[1], content=post[2], id=post[0])

    @classmethod
    def get_all_posts(cls, db_path: str) -> list["Post"]:
        with connect(db_path) as cursor:
            cursor.execute("SELECT * FROM posts")
            return [
                Post(title=row[1], content=row[2], id=row[0])
                for row in cursor.fetchall()
            ]

    @classmethod
    def add_post(cls, title, content, db_path: str) -> None:
        with connect(db_path) as cursor:
            cursor.execute("INSERT INTO posts VALUES (?, ?, ?)", (None, title, content))

    @classmethod
    def update_post(cls, post_id: int, title: str, content: str, db_path: str) -> None:
        with connect(db_path) as cursor:
            cursor.execute(
                "UPDATE posts SET title=?, content=? WHERE id=?",
                (title, content, post_id),
            )

    @classmethod
    def delete_post(cls, post_id: int, db_path: str) -> None:
        with connect(db_path) as cursor:
            cursor.execute("DELETE FROM posts WHERE id=?", (post_id,))

    def __repr__(self):
        return f"Post(title={self.title}, content={self.content}, id={self.id})"


def main():
    Post.create_table("posts.db")
    Post.add_post("Hello", "World", "posts.db")
    Post.add_post("Like", "This", "posts.db")
    Post.add_post("Post", "Here", "posts.db")

    for post in Post.get_all_posts("posts.db"):
        print(post)


if __name__ == "__main__":
    main()
