import sqlite3
from dataclasses import dataclass
from typing import List, Type, Optional, Self

import inject
import pydantic
from pydantic import BaseModel


class Blog(BaseModel):
    title: str = pydantic.Field(min_length=1, max_length=100)
    content: str = pydantic.Field(min_length=1, max_length=1000)
    post_id: Optional[int] = pydantic.Field(default=None, ge=1)


@dataclass
class Repository[ModelType: BaseModel]:
    create_table_sql: str
    create_new_sql: str
    get_sql: str
    update_sql: str
    delete_sql: str
    all_sql: str
    model: Type[ModelType]

    @inject.params(cursor=sqlite3.Cursor)
    def create_table(self, cursor: sqlite3.Cursor) -> Self:
        cursor.execute(self.create_table_sql)
        cursor.connection.commit()
        return self

    @inject.params(cursor=sqlite3.Cursor)
    def create_new(self, model: ModelType, cursor: sqlite3.Cursor) -> ModelType:
        cursor.execute(self.create_new_sql, model.model_dump())
        cursor.connection.commit()
        model.post_id = cursor.lastrowid
        return model

    @inject.params(cursor=sqlite3.Cursor)
    def get(self, post_id: int, cursor: sqlite3.Cursor) -> ModelType:
        cursor.execute(self.get_sql, {"post_id": post_id})
        row = cursor.fetchone()
        if row is None:
            return None
        return self.model.model_validate(dict(row))

    @inject.params(cursor=sqlite3.Cursor)
    def update(self, model: ModelType, cursor: sqlite3.Cursor) -> ModelType:
        cursor.execute(self.update_sql, model.model_dump())
        cursor.connection.commit()
        return model

    @inject.params(cursor=sqlite3.Cursor)
    def delete(self, post_id: int, cursor: sqlite3.Cursor) -> None:
        cursor.execute(self.delete_sql, {"post_id": post_id})
        cursor.connection.commit()

    @inject.params(cursor=sqlite3.Cursor)
    def all(self, cursor: sqlite3.Cursor) -> List[ModelType]:
        cursor.execute(self.all_sql)
        rows = cursor.fetchall()
        return list(map(self.model.model_validate, map(dict, rows)))


@dataclass
class BlogRepository(Repository[Blog]):
    create_table_sql: str = """CREATE TABLE IF NOT EXISTS blogs (
        post_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL
    )"""
    create_new_sql: str = "INSERT INTO blogs (title, content) VALUES (:title, :content)"
    get_sql: str = "SELECT * FROM blogs WHERE post_id = :post_id"
    update_sql: str = (
        "UPDATE blogs SET title = :title, content = :content WHERE post_id = :post_id"
    )
    delete_sql: str = "DELETE FROM blogs WHERE post_id = :post_id"
    all_sql: str = "SELECT * FROM blogs"
    model: Type[Blog] = Blog


@inject.params(repo=BlogRepository)
def create_table(repo: BlogRepository):
    repo.create_table()


@inject.params(repo=BlogRepository)
def create_blog(title: str, content: str, repo: BlogRepository) -> Blog:
    return repo.create_new(Blog(title=title, content=content))


@inject.params(repo=BlogRepository)
def get_blog(post_id: int, repo: BlogRepository) -> Blog:
    return repo.get(post_id)


@inject.params(repo=BlogRepository)
def update_blog(post_id: int, title: str, content: str, repo: BlogRepository) -> Blog:
    return repo.update(Blog(post_id=post_id, title=title, content=content))


@inject.params(repo=BlogRepository)
def delete_blog(post_id: int, repo: BlogRepository) -> None:
    return repo.delete(post_id)


@inject.params(repo=BlogRepository)
def all_blogs(repo: BlogRepository) -> List[Blog]:
    return repo.all()


def init(db: sqlite3.Connection) -> None:
    inject.configure(
        lambda binder: binder.bind_to_constructor(sqlite3.Connection, db)
        .bind_to_provider(sqlite3.Cursor, db.cursor)
        .bind(BlogRepository, BlogRepository())
    )


def main() -> None:
    DATABASE_URL = ":memory:"

    db = sqlite3.connect(DATABASE_URL)
    db.row_factory = sqlite3.Row

    init(db)

    create_table()

    create_blog("Hello", "World")
    post = get_blog(1)
    assert post.title == "Hello", post.title
    assert post.content == "World", post.content
    assert post.post_id == 1, post.post_id

    update_blog(1, "Goodbye", "World")
    post = get_blog(1)
    assert post.title == "Goodbye", post.title
    assert post.content == "World", post.content
    assert post.post_id == 1, post.post_id

    delete_blog(1)
    post = get_blog(1)
    assert post is None, post

    create_blog("Hello", "World")
    create_blog("Goodbye", "World")
    posts = all_blogs()
    assert len(posts) == 2, len(posts)


if __name__ == "__main__":
    main()
