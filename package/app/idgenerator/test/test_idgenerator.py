import unittest
from ..src.idgenerator import IdGenerator


class IdGeneratorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.id_length = 25

    def test_generate_numeric_id(self) -> None:
        num_id = IdGenerator(id_length=self.id_length).generate_numeric_id()
        assert (len(num_id) == self.id_length)
        assert (all(char.isdigit() for char in num_id))

    def test_generate_alphanumeric_id(self) -> None:
        alphanum_id = IdGenerator(id_length=self.id_length).generate_alphanumeric_id()
        assert (len(alphanum_id) == self.id_length)
        assert (all(char.isalpha() for char in alphanum_id))

    def test_generate_mixed_id(self) -> None:
        mixed_id = IdGenerator(id_length=self.id_length).generate_mixed_id()
        assert (len(mixed_id) == self.id_length)
        assert (any(char.isalpha() for char in mixed_id))
        assert (any(char.isalnum() for char in mixed_id))
