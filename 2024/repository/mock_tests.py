import pytest

from post_repo import Post
from with_mock import MockPostRepository


def test_add():
    repo = MockPostRepository()
    repo.add("Hello", "World")
    assert repo.get(0) == Post("Hello", "World", 0)


def test_get_all():
    repo = MockPostRepository()
    repo.add("Hello", "World")
    repo.add("Foo", "Bar")
    assert repo.get_all() == [Post("Hello", "World", 0), Post("Foo", "Bar", 1)]


def test_update():
    repo = MockPostRepository()
    repo.add("Hello", "World")
    repo.update(0, title="Hello World")
    assert repo.get(0) == Post("Hello World", "World", 0)


def test_delete():
    repo = MockPostRepository()
    repo.add("Hello", "World")
    repo.delete(0)
    with pytest.raises(ValueError):
        repo.get(0)


if __name__ == "__main__":
    pytest.main()
