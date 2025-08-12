from singleton import Singleton


class Config(metaclass=Singleton):
    def __init__(self):
        self.db_url = "sqlite:///:memory:"
        self.debug = True

    def __str__(self) -> str:
        return f"Config(db_url={self.db_url}, debug={self.debug})"


def main() -> None:
    s1 = Config()
    s2 = Config()

    print(s1 is s2)  # Should print True, indicating both are the same instance
    print(id(s1))  # Prints the instance id
    print(id(s2))  # Prints the same instance id as s1


if __name__ == "__main__":
    main()
