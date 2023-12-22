import unittest.mock
from post_repo import Post
from with_mock import MockPostRepository


class TesPostRepository(unittest.TestCase):

    def setUp(self):
        self.repo = MockPostRepository(":memory:")

    def test_add(self):
        self.repo.add(Post("Hello", "World"))
        self.assertEqual(len(self.repo.posts), 1)
        self.repo.delete(Post("Hello", "World", 0))

    def test_get(self):
        self.repo.add(Post("Hello", "World"))
        self.assertEqual(self.repo.get(0), Post("Hello", "World"))
        self.repo.delete(Post("Hello", "World", 0))

    def test_get_all(self):
        self.repo.add(Post("Hello", "World"))
        self.repo.add(Post("Hello", "World"))
        self.repo.add(Post("Hello", "World"))
        self.assertEqual(len(self.repo.get_all()), 3)
        self.repo.delete(Post("Hello", "World", 0))
        self.repo.delete(Post("Hello", "World", 1))
        self.repo.delete(Post("Hello", "World", 2))

    def test_update(self):
        self.repo.add(Post("Hello", "World"))
        self.repo.update(Post("Hello", "World", 0))
        self.assertEqual(self.repo.get(0), Post("Hello", "World", 0))
        self.repo.delete(Post("Hello", "World", 0))

    def test_delete(self):
        self.repo.add(Post("Hello", "World"))
        self.repo.delete(Post("Hello", "World", 0))
        self.assertEqual(len(self.repo.posts), 0)

    
if __name__ == "__main__":
    unittest.main()
