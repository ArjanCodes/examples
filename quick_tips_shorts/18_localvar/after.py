import random
from dataclasses import dataclass


@dataclass
class NumbersGame:
    answer: int = random.randint(1, 10)

    def place_a_guess(self) -> bool:
        guess = int(input("Guess a number: "))

        if guess == self.answer:
            print("You win!")
        elif guess < self.answer:
            print("Too low!")
        else:
            print("Too high!")

        return guess == self.answer

    def play(self):
        guesses = 5
        print("I'm thinking of a number between 1 and 10.")
        print(f"You have {guesses} guesses.")
        print("Ready? Go!")

        while guesses > 0 and not self.place_a_guess():
            guesses -= 1
            print(f"Player has {guesses} guesses left.")
        if guesses <= 0:
            print(f"You lost! The number was {self.answer}.")


def main():
    game = NumbersGame()
    game.play()


if __name__ == "__main__":
    main()
