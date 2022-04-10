import random


def place_a_guess(answer: int) -> bool:
    while True:
        try:
            guess = int(input("Guess a number: "))

            if guess == answer:
                print("You win!")
            elif guess < answer:
                print("Too low!")
            else:
                print("Too high!")

            return guess == answer
        except ValueError:
            print("That's not a number!")


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
