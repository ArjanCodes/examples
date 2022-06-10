class Greeting:
    def __init__(self, greeting_type: str) -> None:
        self.greeting_type = greeting_type

    def greet(self, name: str) -> str:
        return self.greeting_type + ", " + name

    def greet_list(self, names: list[str]) -> list[str]:
        greetings: list[str] = []
        for name in names:
            greetings.append(self.greet(name))
        return greetings


def main():
    name = input("Enter your name: ")
    greeting = Greeting("Hello")
    print(greeting.greet(name))
    print("\n".join(greeting.greet_list(["John", "Jane", "Joe"])))


if __name__ == "__main__":
    main()
