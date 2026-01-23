import re
from dataclasses import dataclass

EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


@dataclass(frozen=True)
class EmailAddress:
    value: str

    def __post_init__(self) -> None:
        if not EMAIL_RE.match(self.value):
            raise ValueError(f"Invalid email address: {self.value}")

    @property
    def domain(self) -> str:
        return self.value.split("@", 1)[1]


def main() -> None:
    email = EmailAddress("hello@example.com")
    print(email.domain)  # example.com

    # EmailAddress("not-an-email")  # raises ValueError


if __name__ == "__main__":
    main()
