def greet(name: str, greeting_type: str) -> str:
    return greeting_type + ", " + name


def greet_list(names: list[str], greeting_type: str) -> list[str]:
    return [greet(name, greeting_type) for name in names]


def main():
    greeting_type = "Hello"
    name = input("Enter your name: ")
    print(greet(name, greeting_type))
    print(greet_list(["John", "Jane", "Joe"], greeting_type))


if __name__ == "__main__":
    main()
