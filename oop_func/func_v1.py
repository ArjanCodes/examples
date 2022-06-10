from datetime import datetime


def greet(name: str, greeting_intro: str) -> str:
    return f"{greeting_intro}, {name}."


def greet_friendly(name: str, greeting_intro: str) -> str:
    return f"{greeting_intro}, {name}. How are you doing?"


def greet_list(names: list[str], greeting_intro: str) -> list[str]:
    return [greet(name, greeting_intro) for name in names]


def main() -> None:
    current_time = datetime.now()
    if current_time.hour < 12:
        greeting_intro = "Good morning"
    elif 12 <= current_time.hour < 18:
        greeting_intro = "Good afternoon"
    else:
        greeting_intro = "Good evening"

    name = input("Enter your name: ")
    print(greet(name, greeting_intro))
    print(greet_list(["John", "Jane", "Joe"], greeting_intro))


if __name__ == "__main__":
    main()
