from datetime import datetime


class Greeting:
    def __init__(self) -> None:
        current_time = datetime.now()
        if current_time.hour < 12:
            self.greeting_intro = "Good morning"
        elif 12 <= current_time.hour < 18:
            self.greeting_intro = "Good afternoon"
        else:
            self.greeting_intro = "Good evening"

    def greet(self, name: str) -> None:
        print(f"{self.greeting_intro}, {name}.")

    def greet_list(self, names: list[str]) -> None:
        for name in names:
            self.greet(name)


class FriendlyGreeting(Greeting):
    def greet(self, name: str) -> None:
        print(f"{self.greeting_intro}, {name}. How are you doing?")


def main() -> None:
    name = input("Enter your name: ")

    greeting = FriendlyGreeting()
    greeting.greet(name)
    greeting.greet_list(["John", "Jane", "Joe"])


if __name__ == "__main__":
    main()
