import unittest
import unittest.mock
from repository import PostRepository

class TestPostRepository(unittest.TestCase):
    def setUp(self):
        self.repo = PostRepository(":memory:")

    def test_add(self):
        self.repo.add("Hello", "World")
        self.assertEqual(self.repo.get(0), Post("Hello", "World", 0))

    def test_get(self):
        self.repo.add("Hello", "World")
        self.assertEqual(self.repo.get(0), Post("Hello", "World", 0))

    def test_get_all(self):
        self.repo.add("Hello", "World")
        self.repo.add("Foo", "Bar")
        self.assertEqual(self.repo.get_all(), [Post("Hello", "World", 0), Post("Foo", "Bar", 1)])

    def test_update(self):
        self.repo.add("Hello", "World")
        self.repo.update(0, title = "Hello World")
        self.assertEqual(self.repo.get(0), Post("Hello World", "World", 0))

    def test_delete(self):
        self.repo.add("Hello", "World")
        self.repo.delete(0)
        with self.assertRaises(ValueError):
            self.repo.get(0)
