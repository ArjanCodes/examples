from dataclasses import dataclass


@dataclass
class ChessPiece:
    color: str
    name: str


class Chessboard:
    """
    Class Invariants:
        - The board dimensions are always 8x8 squares.
        - All pieces are positioned within the valid boundaries of the chessboard.
        - Each player has exactly one king on the board at all times, until the king is checkmated or the game ends in a stalemate.
        - A player can have at most one queen, two bishops, two knights, two rooks, and eight pawns in a standard game of chess.

    """

    def __init__(self):
        self.board: list[list[ChessPiece | None]] = self.create_board()

    @staticmethod
    def create_board() -> list[list[ChessPiece | None]]:
        return [[None for _ in range(8)] for _ in range(8)]

    def place_piece(self, row: int, col: int, piece: ChessPiece) -> None:
        if 0 <= row < 8 and 0 <= col < 8:  # Check within bounds
            if self.board[row][col] is None:  # Square is empty
                self.board[row][col] = piece
            else:
                raise ValueError("Square is already occupied.")
        else:
            raise ValueError("Position is out of bounds.")

    def is_occupied(self, row: int, col: int) -> bool:
        if 0 <= row < 8 and 0 <= col < 8:  # Check within bounds
            return self.board[row][col] is not None
        else:
            raise ValueError("Position is out of bounds.")

    def can_place_bishop(self, row: int, col: int, color: str) -> bool:
        square_color = (row + col) % 2  # 0 for dark squares, 1 for light squares
        for r in range(8):
            for c in range(8):
                if (r + c) % 2 == square_color:
                    piece = self.board[r][c]

                    if not piece:
                        continue

                    if piece.name.lower() == "bishop" and piece.color == color:
                        return False  # Found another bishop of the same color on the same color square
        return True

    def __str__(self) -> str:
        board_str = ""
        for row in self.board:
            for square in row:
                piece = square if square else "Empty"
                board_str += f"{piece}\t"
            board_str += "\n"
        return board_str


def main() -> None:
    chessboard = Chessboard()
    print(chessboard)


if __name__ == "__main__":
    main()
