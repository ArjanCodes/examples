import pytest
from with_mock import MockPostRepository
from post_repo import Post

def test_add():
    repo = MockPostRepository(":memory:")
    repo.add("Hello", "World")
    assert repo.get(0) == Post("Hello", "World", 0)
    
def test_get_all():
    repo = MockPostRepository(":memory:")
    repo.add("Hello", "World")
    repo.add("Foo", "Bar")
    assert repo.get_all() == [Post("Hello", "World", 0), Post("Foo", "Bar", 1)]
    
def test_update():
    repo = MockPostRepository(":memory:")
    repo.add("Hello", "World")
    repo.update(0, title = "Hello World")
    assert repo.get(0) == Post("Hello World", "World", 0)
    
def test_delete():
    repo = MockPostRepository(":memory:")
    repo.add("Hello", "World")
    repo.delete(0)
    with pytest.raises(ValueError):
        repo.get(0)
        
def test_repr():
    repo = MockPostRepository(":memory:")
    assert repr(repo) == "MockPostRepository(db_path=:memory:)"
    
def test_create_table():
    repo = MockPostRepository(":memory:")
    repo.create_table()
    assert repo.get_all() == []
    
    
if __name__ == "__main__":
    pytest.main()
