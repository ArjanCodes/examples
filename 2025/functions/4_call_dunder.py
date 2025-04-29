class Greeter:
    def __call__(self, name: str) -> str:
        return f"Hello, {name}!"


def main() -> None:
    greet = Greeter()
    print(greet("Alice"))  # Output: "Hello, Alice!"


if __name__ == "__main__":
    main()
