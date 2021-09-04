import random
import string
from dataclasses import dataclass, field


def generate_id(length: int = 8):
    """Helper function for generating an id."""
    return "".join(random.choices(string.ascii_uppercase, k=length))


@dataclass
class SupportTicket:
    customer: str
    issue: str
    id: str = field(init=False)

    def __post_init__(self):
        self.id = generate_id()

    def process(self):
        print("==================================")
        print(f"Processing ticket id: {self.id}")
        print(f"Customer: {self.customer}")
        print(f"Issue: {self.issue}")
        print("==================================")
