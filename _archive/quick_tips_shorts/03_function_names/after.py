def read_name() -> str:
    return input("Enter your name: ")


def read_age() -> int:
    while True:
        line = input("Enter your age: ")
        try:
            return int(line)
        except ValueError:
            print("That's not a number! Try again.")


def evaluate_age(name: str, age: int) -> None:
    young_cutoff = 30
    if age <= young_cutoff:
        print(f"{name}, you are young.")
    else:
        print(f"{name}, you're old!")


def main():
    name = read_name()
    age = read_age()
    evaluate_age(name, age)


if __name__ == "__main__":
    main()
