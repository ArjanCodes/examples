import unittest
import string
from ..src.idgenerator import (
    generate_password,
    generate_guid,
    generate_credit_card_number,
    generate_object_id,
    generate_pin_number,
)
from ..src.utils import luhn_checksum


class GeneratorTest(unittest.TestCase):
    def test_generate_password(self) -> None:
        pwd = generate_password(length=6)
        self.assertTrue(
            (any(char.isupper() for char in pwd))
            and (any(char.islower() for char in pwd))
            and (any(char in string.punctuation for char in pwd))
            and (any(char in string.digits for char in pwd))
        )
        self.assertRaises(AssertionError, generate_password, length=5)

    def test_generate_guid(self) -> None:
        guid = generate_guid()
        parts = guid.split("-")
        self.assertTrue(len(parts) == 5)
        criteria = [char in string.hexdigits for part in parts for char in part]
        self.assertTrue(all(criteria))
        self.assertTrue(len(parts[0]) == 8)
        self.assertTrue(len(parts[1]) == 4)
        self.assertTrue(len(parts[2]) == 4)
        self.assertTrue(len(parts[3]) == 4)
        self.assertTrue(len(parts[4]) == 12)

    def test_generate_credit_card_number(self) -> None:
        number = generate_credit_card_number()
        self.assertTrue(luhn_checksum(number))

    def test_generate_pin_number(self) -> None:
        self.assertTrue(len(generate_pin_number(length=4)) == 4)
        self.assertTrue(
            all(digits in string.digits for digits in generate_pin_number(length=4))
        )

    def test_generate_object_id(self) -> None:
        objid = generate_object_id()
        self.assertTrue(len(objid) == 24)
        self.assertTrue(all(char in string.hexdigits for char in objid))
