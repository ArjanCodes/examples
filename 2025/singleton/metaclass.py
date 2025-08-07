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
    s1 = Config()
    s2 = Config()

    print(s1 is s2)  # Should print True, indicating both are the same instance
    print(id(s1))  # Prints the instance id
    print(id(s2))  # Prints the same instance id as s1

if __name__ == "__main__":
    main()