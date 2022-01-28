# Battleship Attempt 2

# Imports

import os
import random as rand

GUESSES_COUNT = 5
BOARD_SIZE = 5


def read_int(prompt: str, min_value: int = 1, max_value: int = 5) -> int:
    line = input(prompt)
    try:
        value = int(line)
        if value < min_value:
            print(f"The minimum value is {min_value}. Try again.")
        elif value > max_value:
            print(f"The maximum value is {max_value}. Try again.")
        else:
            return value
    except ValueError:
        print("That's not a number! Try again.")
    return read_int(prompt)


"""
Defining the Game class to make it easier to 
understand the code further in the project
"""


class Game:
    def __init__(self, player_count: int):
        self.player_list = [GUESSES_COUNT] * player_count
        self.current_player = 1
        self.board = self.create_board(BOARD_SIZE, BOARD_SIZE)
        self.ship_row = rand.randint(0, BOARD_SIZE - 1)
        self.ship_col = rand.randint(0, BOARD_SIZE - 1)

    """
    Defining the many methods that makes the game work,
    starting with the create_matrix where we take in the 
    boards max x and max y to define its size.
    """

    def create_board(self, max_x: int, max_y: int) -> list[str]:
        return ["O" * max_x] * max_y

    def is_ship(self, row: int, col: int) -> bool:
        return row == self.ship_row and col == self.ship_col

    def already_guessed(self, row: int, col: int) -> bool:
        return self.board[row][col] == "X"

    def place_guess_on_board(self, row: int, col: int):
        current_row = self.board[row]
        self.board[row] = current_row[:col] + "X" + current_row[col + 1 :]

    @property
    def current_player_guesses_remaining(self) -> int:
        return self.player_list[self.current_player - 1]

    """
    Defining the print_board function, here I respresent
    x as rows
    y as colums
    """

    def print_board(self, show_ship: bool = False):
        for row in self.board:
            if row == self.ship_row and show_ship:
                ship_row = self.board[self.ship_row]
                print(
                    " ".join(
                        ship_row[: self.ship_col] + "S" + ship_row[self.ship_col + 1 :]
                    )
                )
            else:
                print(" ".join(row))

    """
    I wanted to avoid retyping code as much as possible
    so I did the above function and then created player_guesses
    to take user input and sort it into guesses for row and column
    As of writing this comment I'm avoiding writing any game logic in the function.
    """

    def player_guess(self) -> tuple[int, int]:

        guess_row = read_int(
            f"Player {self.current_player}: Guess row: ", max_value=BOARD_SIZE
        )
        guess_col = read_int(
            f"Player {self.current_player}: Guess column: ", max_value=BOARD_SIZE
        )

        if self.already_guessed(guess_row, guess_col):
            print("You've already guessed on that row! Try again.")
            return self.player_guess()

        # reduce guesses by 1
        self.player_list[self.current_player - 1] -= 1

        # place the guess on the board
        self.place_guess_on_board(guess_row, guess_col)

        # return the guessed row and column
        return guess_row, guess_col

    """
    Seperating out the game_logic to try to make the main function as readable as possible.
    This is also an exercise to practice writing recursive code instead of using while loops.
    """

    def main(self):
        while True:
            if self.current_player_guesses_remaining <= 0:
                print(f"Player {self.current_player} ran out of guesses and lost!")
                break

            # print the board
            self.print_board()

            # let the player guess
            print(
                f"Player {self.current_player} has {self.current_player_guesses_remaining} guesses left."
            )
            guess_row, guess_col = self.player_guess()

            # if you found the ship, you win
            if self.is_ship(guess_row, guess_col):
                print(f"Congratulations! Player {self.current_player} sank the ship!")
                break

            print("Sorry, you missed!")

            # go to the next player
            self.current_player = (self.current_player % len(self.player_list)) + 1

        # print the board one last time, showing the ship
        self.print_board(show_ship=True)


"""
Here is all that is left outside of functions and the game class. 
Pretty easy to read if you ask me.
"""


def main():
    os.system("clear")
    player_count = read_int(
        "Please enter how many players are going to play:", max_value=2
    )
    game = Game(player_count)
    os.system("clear")
    game.main()


if __name__ == "__main__":
    main()
