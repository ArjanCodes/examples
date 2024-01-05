import typing
from repository import Repository
from post_repo import Post


class MockPostRepository(Repository[Post]):
    def __init__(self, db_path: str, posts: typing.Optional[dict[int, Post]] = None):
        super().__init__(db_path)
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

    def create_table(self) -> None:
        """Since we are using a dictionary, we don't need to create a table"""
        pass


def main():
    repo = MockPostRepository("../../posts.db")
    repo.add(Post("Hello", "World"))
    repo.add(Post("Hello", "World"))
    repo.add(Post("Hello", "World"))

    print(repo.get_all())
    print(repo.get(1))
    repo.update(Post("Hello", "World", 1))
    print(repo.get(1))


if __name__ == "__main__":
    main()
