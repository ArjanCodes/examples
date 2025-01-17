import random
import string


def random_string(length: int = 8) -> str:
    """Generate a random string of fixed length"""
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for i in range(length))
