from dataclasses import InitVar, dataclass


@dataclass
class UserWithPassword:
    email: str
    raw_password: InitVar[str]
    password_hash: int = 0

    def __post_init__(self, raw_password: str) -> None:
        self.password_hash = hash(raw_password)


def main() -> None:
    u = UserWithPassword("alice@test.com", "super-secret")

    print(u.email)
    print(u.password_hash)
    # print(u.raw_password)  # AttributeError


if __name__ == "__main__":
    main()
