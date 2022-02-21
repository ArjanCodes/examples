import random
from dataclasses import dataclass


@dataclass
class NumbersGame:
    guesses: int = 5
    answer: int = random.randint(1, 10)

    def read_integer(self) -> int:
        return int(input("Guess a number: "))

    def place_a_guess(self) -> bool:
        guess = self.read_integer()
        if guess == self.answer:
            print("You win!")
        elif guess < self.answer:
            print("Too low!")
        else:
            print("Too high!")

        return guess == self.answer

    def play(self) -> None:
        print("I'm thinking of a number between 1 and 10.")
        print(f"You have {self.guesses} guesses.")
        print("Ready? Go!")

        while self.guesses > 0 and not self.place_a_guess():
            self.guesses -= 1
            print(f"Player has {self.guesses} guesses left.")
        if self.guesses <= 0:
            print(f"You lost! The number was {self.answer}.")


def main():
    game = NumbersGame()
    game.play()


if __name__ == "__main__":
    main()
