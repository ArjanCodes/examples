import random
import string
import secrets  # To generate cryptographic safe passwords
import uuid
from .utils import luhn_checksum
import bson


def generate_password(length: int = 6) -> str:
    """
    A generator that creates a password of at least 6 characters and contains
    at least one uppercase & lowercase letter, 1 number and at 1 symbol

    """
    assert length >= 6, f"Password length can't be less than 6, {length} given!"
    while True:
        pwd = ""
        for i in range(length):
            pwd += "".join(
                secrets.choice(
                    string.ascii_letters + string.digits + string.punctuation
                )
            )
        if (
            (any(char.isupper() for char in pwd))
            and (any(char.islower() for char in pwd))
            and (any(char in string.punctuation for char in pwd))
            and (any(char in string.digits for char in pwd))
        ):
            break

    return pwd


def generate_guid() -> str:
    """
    A generator that creates a GUID.

    """
    guid = str(uuid.uuid4())
    guid = guid.upper()
    return guid


def generate_credit_card_number(length: int = 8) -> str:
    """
    A credit card number generator that uses the Luhn checksum test.

    """
    number = "".join(random.choices(string.digits, k=length))
    while not luhn_checksum(number):
        number = "".join(random.choices(string.digits, k=length))
    return number


def generate_pin_number(length: int = 4) -> str:
    """
    A credit/debit card pin generator. The pin number can only contain digits.

    """
    return "".join(random.choices(string.digits, k=length))


def generate_object_id() -> str:
    """
    A generator that creates a mongodb like objectID.
    An ObjectId is a 12-byte unique identifier consisting of:

          - a 4-byte value representing the seconds since the Unix epoch,
          - a 3-byte machine identifier,
          - a 2-byte process id, and
          - a 3-byte counter, starting with a random value.

    """
    return str(bson.ObjectId())
