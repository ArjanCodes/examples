import random
import string
from typing import Callable


def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


BufferData = str

Buffer = Callable[[], BufferData]
