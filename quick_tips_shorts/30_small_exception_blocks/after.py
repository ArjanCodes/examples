import random


def read_int() -> int:
    while True:
        try:
            return int(input("Guess a number: "))
        except ValueError:
            print("That's not a number!")


def place_a_guess(answer: int) -> bool:
    guess = read_int()

    if guess == answer:
        print("You win!")
    elif guess < answer:
        print("Too low!")
    else:
        print("Too high!")

    return guess == answer


def main():
    guesses = 5
    answer = random.randint(1, 10)
    print("I'm thinking of a number between 1 and 10.")
    print(f"You have {guesses} guesses.")
    print("Ready? Go!")

    while guesses > 0:
        print(f"You have {guesses} guesses left.")
        if place_a_guess(answer):
            break
        guesses -= 1


if __name__ == "__main__":
    main()
