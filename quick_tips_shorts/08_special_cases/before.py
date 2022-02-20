import random


def place_a_guess(guesses: int, answer: int, player_name: str) -> bool:
    if guesses > 0:
        print(f"Player {player_name} has {guesses} guesses left.")

        guess = int(input("Guess a number: "))
        if guess == answer:
            print("You win!")
            return True
        else:
            if guess < answer:
                print("Too low!")
            else:
                print("Too high!")
            return False
    else:
        return False


def main():
    name = input("What is your name? ")
    guesses = 5
    answer = random.randint(1, 10)
    print(f"Hello, {name}!")
    print("I'm thinking of a number between 1 and 10.")
    print(f"You have {guesses} guesses.")
    print("Ready? Go!")

    while guesses > 0:
        if place_a_guess(guesses, answer, name):
            break
        guesses -= 1


if __name__ == "__main__":
    main()
