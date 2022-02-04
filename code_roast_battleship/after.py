import os
import random

GUESSES_COUNT = 5
BOARD_SIZE_X = 5
BOARD_SIZE_Y = 5


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


def create_board(size_x: int, size_y: int) -> list[list[str]]:
    # create the board
    board = [["O"] * size_x for _ in range(size_y)]

    # place the ship on the board
    ship_row = random.randint(0, size_x - 1)
    ship_col = random.randint(0, size_y - 1)
    board[ship_row][ship_col] = "S"

    return board


class Game:
    """
    Defining the Game class to make it easier to
    understand the code further in the project"""

    def __init__(self, player_count: int = 1) -> None:
        self.player_count = player_count
        self.board = create_board(BOARD_SIZE_X, BOARD_SIZE_Y)

    def is_ship(self, row: int, col: int) -> bool:
        return self.board[row][col] == "S"

    def already_guessed(self, row: int, col: int) -> bool:
        return self.board[row][col] == "X"

    def place_guess_on_board(self, row: int, col: int) -> None:
        if not self.is_ship(row, col):
            self.board[row][col] = "X"

    def print_board(self, show_ship: bool = False):
        for row in self.board:
            row = ["O" if col == "S" and not show_ship else col for col in row]
            print(" ".join(row))

    def read_player_guess(self, player: int) -> tuple[int, int]:

        guess_row = (
            read_int(f"Player {player}: Guess row: ", max_value=BOARD_SIZE_X) - 1
        )
        guess_col = (
            read_int(f"Player {player}: Guess column: ", max_value=BOARD_SIZE_Y) - 1
        )

        if self.already_guessed(guess_row, guess_col):
            print("You've already guessed on that row! Try again.")
            return self.read_player_guess(player)

        # return the guessed row and column
        return guess_row, guess_col

    def turn(self, player: int) -> bool:

        # print the board
        self.print_board()

        # let the player guess
        guess_row, guess_col = self.read_player_guess(player)

        # if you found the ship, you win
        if self.is_ship(guess_row, guess_col):
            print(f"Congratulations! Player {player} sank the ship!")
            return True

        # you didn't find the ship, so place the guess on the board
        self.place_guess_on_board(guess_row, guess_col)
        print("Sorry, you missed!")
        return False

    def main(self) -> None:
        total_guesses = 0
        while total_guesses < GUESSES_COUNT * self.player_count:

            # determine the current player and the remaining guesses
            current_player = (total_guesses % self.player_count) + 1
            remaining_guesses = GUESSES_COUNT - total_guesses // self.player_count

            print(f"Player {current_player} has {remaining_guesses} guesses left.")

            if self.turn(current_player):
                break
            total_guesses += 1

        # print the board one last time, showing the ship
        self.print_board(show_ship=True)


def main():
    os.system("clear")
    player_count = read_int(
        "Please enter how many players are going to play: ", max_value=2
    )
    game = Game(player_count)
    os.system("clear")
    game.main()


if __name__ == "__main__":
    main()
