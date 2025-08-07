class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            print(f"Creating instance of {cls.__name__}")
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

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

