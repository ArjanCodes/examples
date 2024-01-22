import typing

from after import Post
from repository import Repository


class MockPostRepository(Repository[Post]):
    def __init__(self, posts: typing.Optional[dict[int, Post]] = None):
        self.posts = posts or {}

    def get(self, id_: int) -> Post:
        return self.posts[id_]

    def get_all(self) -> list[Post]:
        return list(self.posts.values())

    def add(self, entry: Post) -> None:
        self.posts[len(self.posts)] = entry

    def update(self, entry: Post) -> None:
        if entry.id is None:
            raise ValueError("Cannot update a post without an id")
        self.posts[entry.id] = entry

    def delete(self, entry: Post) -> None:
        if entry.id is None:
            raise ValueError("Cannot delete a post without an id")
        del self.posts[entry.id]


def main():
    repo = MockPostRepository()
    repo.add(Post("Hello", "World"))
    repo.add(Post("Hello", "World"))
    repo.add(Post("Hello", "World"))

    print(repo.get_all())
    print(repo.get(1))
    repo.update(Post("Hello", "World", 1))
    print(repo.get(1))


if __name__ == "__main__":
    main()
