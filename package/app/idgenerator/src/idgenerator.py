import random
import string
from dataclasses import dataclass


@dataclass
class IdGenerator:
    id_length: int = 6

    def generate_numeric_id(self) -> str:
        """
        A generator that creates numerical ids of variable lengths

        """
        return ''.join(random.choices(string.digits, k=self.id_length))

    def generate_alphanumeric_id(self) -> str:
        """
        A generator that creates alphanumerical ids of variable lengths

        """
        return ''.join(
            random.choices(string.ascii_letters, k=self.id_length))

    def generate_mixed_id(self) -> str:
        """
        A generator that creates mixed ids of variable lengths

        """
        return ''.join(
            random.choices(string.ascii_letters + string.hexdigits + string.punctuation, k=self.id_length))
