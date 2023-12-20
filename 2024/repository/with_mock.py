import typing
import sqlite3
import abc
import contextlib

RepoObject = typing.TypeVar('RepoObject')


class Repository(typing.Generic[RepoObject], metaclass = abc.ABCMeta):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.create_table()

    @contextlib.contextmanager
    def connect(self):
        with sqlite3.connect(self.db_path) as conn:
            yield conn.cursor()

    @abc.abstractmethod
    def get(self, id: int) -> RepoObject:
        ...

    @abc.abstractmethod
    def get_all(self) -> typing.List[RepoObject]:
        ...

    @abc.abstractmethod
    def add(self, *args, **kwargs) -> None:
        ...

    @abc.abstractmethod
    def update(self, id: int, **kwargs) -> None:
        ...

    @abc.abstractmethod
    def delete(self, id: int) -> None:
        ...

    @abc.abstractmethod
    def create_table(self) -> None:
        ...


class Post:
    def __init__(self, title: str, content: str, id: int = None):
        self.id = id
        self.title = title
        self.content = content

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title}, content={self.content})"


class PostRepository(Repository[Post]):
    def create_table(self) -> None:
        with self.connect() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, title TEXT, content TEXT)")

    def get(self, id: int) -> Post:
        with self.connect() as cursor:
            cursor.execute("SELECT * FROM posts WHERE id=?", (id,))
            post = cursor.fetchone()
            if post is None:
                raise ValueError(f"Post with id {id} does not exist")
            return Post(title = post[1], content = post[2], id = post[0])

    def get_all(self) -> typing.List[Post]:
        with self.connect() as cursor:
            cursor.execute("SELECT * FROM posts")
            return [Post(title = row[1], content = row[2], id = row[0]) for row in cursor.fetchall()]

    def add(self, title, content) -> None:
        with self.connect() as cursor:
            cursor.execute("INSERT INTO posts VALUES (?, ?, ?)", (None, title, content))

    def update(self, id: int, content = None, title = None) -> None:
        if content is None and title is None:
            raise ValueError("Must provide either content or title")
        with self.connect() as cursor:
            if content is not None and title is not None:
                cursor.execute("UPDATE posts SET title=?, content=? WHERE id=?", (title, content, id))
            elif content is not None:
                cursor.execute("UPDATE posts SET content=? WHERE id=?", (content, id))
            else:
                cursor.execute("UPDATE posts SET title=? WHERE id=?", (title, id))

    def delete(self, id: int) -> None:
        with self.connect() as cursor:
            cursor.execute("DELETE FROM posts WHERE id=?", (id,))

    def __repr__(self):
        return f"PostRepository(db_path={self.db_path})"

class MockPostRepository(Repository[Post]):
    def __init__(self, db_path: str, posts=None):
        super().__init__(db_path)
        self.posts = posts or {}

    def create_table(self) -> None:
        pass

    def get(self, id: int) -> Post:
        return self.posts[id]

    def get_all(self) -> typing.List[Post]:
        return list(self.posts.values())

    def add(self, title, content) -> None:
        id = len(self.posts)
        self.posts[id] = Post(title, content, id)

    def update(self, id: int, content = None, title = None) -> None:
        if content is None and title is None:
            raise ValueError("Must provide either content or title")
        post = self.posts[id]
        if content is not None:
            post.content = content
        if title is not None:
            post.title = title

    def delete(self, id: int) -> None:
        del self.posts[id]

    def __repr__(self):
        return f"MockPostRepository(db_path={self.db_path})"

def main(repo):
    repo.add("Hello", "World")
    repo.add("Foo", "Bar")
    print(repo.get_all())
    repo.update(0, title = "Hello World")
    print(repo.get_all())
    repo.delete(1)
    print(repo.get_all())


if __name__ == "__main__":
    repo = MockPostRepository("posts.db")
    main(repo)
