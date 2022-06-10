def greet(name: str, greeting_type: str) -> str:
    return greeting_type + ", " + name


def greet_list(names: list[str], greeting_type: str) -> list[str]:
    return [greet(name, greeting_type) for name in names]


def get_greeting_type() -> str:
    return "Hello"


def read_name() -> str:
    return input("Enter your name: ")


def main():
    print(greet(read_name(), get_greeting_type()))
    print(greet_list(["John", "Jane", "Joe"], get_greeting_type()))


if __name__ == "__main__":
    main()
