from singleton import Singleton


class Config(metaclass=Singleton):
    def __init__(self):
        self.db_url = "sqlite:///:memory:"
        self.debug = True

    def __str__(self) -> str:
        return f"Config(db_url={self.db_url}, debug={self.debug})"


def main() -> None:
    c1 = Config()
    c2 = Config.__new__(Config)
    c2.__init__()

    print(c1 is c2)  # ❌ False


if __name__ == "__main__":
    main()
