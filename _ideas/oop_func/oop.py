class Greeting:
    def __init__(self, greeting_type: str) -> None:
        self.greeting_type = greeting_type

    def greet(self, name: str) -> None:
        print(self.greeting_type + ", " + name)

    def greet_list(self, names: list[str]) -> None:
        for name in names:
            self.greet(name)


def main():
    name = input("Enter your name: ")
    greeting = Greeting("Hello")
    greeting.greet(name)
    greeting.greet_list(["John", "Jane", "Joe"])


if __name__ == "__main__":
    main()
