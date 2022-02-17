def first_step() -> str:
    return input("Enter your name: ")


def second_step() -> int:
    while True:
        line = input("Enter your age: ")
        try:
            return int(line)
        except ValueError:
            print("That's not a number! Try again.")


def final_step(name: str, age: int) -> None:
    young_cutoff = 30
    if age <= young_cutoff:
        print(f"{name}, you are young.")
    else:
        print(f"{name}, you're old!")


def main():
    name = first_step()
    age = second_step()
    final_step(name, age)


if __name__ == "__main__":
    main()
