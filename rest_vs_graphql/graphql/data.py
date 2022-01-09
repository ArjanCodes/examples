from typing import TypedDict


class Blog(TypedDict):
    id: int
    title: str
    content: str
    author_id: int


class BlogPayload(TypedDict, total=False):
    title: str
    content: str


class Author(TypedDict):
    id: int
    name: str


BLOGS: dict[int, Blog] = {
    1: {"id": 1, "title": "Blog 1", "author_id": 1, "content": "Content 1"},
    2: {"id": 2, "title": "Blog 2", "author_id": 2, "content": "Content 2"},
    3: {"id": 3, "title": "Blog 3", "author_id": 3, "content": "Content 3"},
}

AUTHORS: dict[int, Author] = {
    1: {"id": 1, "name": "Author 1"},
    2: {"id": 2, "name": "Author 2"},
    3: {"id": 3, "name": "Author 3"},
}


class NotFoundError(Exception):
    pass


def all_blogs() -> list[Blog]:
    return list(BLOGS.values())


def get_blog(blog_id: int) -> Blog:
    if not BLOGS.get(blog_id):
        raise NotFoundError("Blog not found")
    return BLOGS[blog_id]


def update_blog(blog_id: int, payload: BlogPayload) -> Blog:
    blog = BLOGS.get(blog_id)
    if not blog:
        raise NotFoundError("Blog not found")
    for key, value in payload.items():
        blog[key] = value
    return blog


def all_authors() -> list[Author]:
    return list(AUTHORS.values())


def get_author(author_id: int) -> Author:
    if not AUTHORS.get(author_id):
        raise NotFoundError("Author not found")
    return AUTHORS[author_id]
