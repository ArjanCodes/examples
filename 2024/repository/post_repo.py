from dataclasses import dataclass
from repository import Repository
from typing import Optional

@dataclass
class Post:
    title: Optional[str] = None
    content: Optional[str] = None
    id: Optional[int] = None


class PostRepository(Repository[Post]):
    def create_table(self) -> None:
        with self.connect() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, title TEXT, content TEXT)")

    def add(self, entry: Post) -> None:
        with self.connect() as cursor:
            cursor.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (entry.title, entry.content))

    def get(self, id_: int) -> Post:
        with self.connect() as cursor:
            cursor.execute("SELECT * FROM posts WHERE id = ?", (id_,))
            entry = cursor.fetchone()
            return Post(title=entry[1], content=entry[2], id=entry[0])
        
    def get_all(self) -> list[Post]:
        with self.connect() as cursor:
            cursor.execute("SELECT * FROM posts")
            entries = cursor.fetchall()
            return [Post(entry[1], entry[2]) for entry in entries]
        
    def update(self, entry: Post) -> None:
        if entry.id is None:
            raise ValueError("Cannot update a post without an id")
        with self.connect() as cursor:
            cursor.execute("UPDATE posts SET title = ?, content = ? WHERE id = ?", (entry.title, entry.content, entry.id))

    def delete(self, entry: Post) -> None:
        if entry.id is None:
            raise ValueError("Cannot delete a post without an id")
        with self.connect() as cursor:
            cursor.execute("DELETE FROM posts WHERE id = ?", (entry.id,))

            

        
def main():
    repo = PostRepository("../../posts.db")
    repo.add(Post("Hello", "World"))
    repo.add(Post("Hello", "World"))
    repo.add(Post("Hello", "World"))

    print(repo.get_all())
    print(repo.get(1))
    repo.update(Post("Hello", "World", 1))
    print(repo.get(1))


if __name__ == "__main__":
    main()
