from dataclasses import dataclass
from enum import Enum
from typing import Self


class PieceType(Enum):
    EMPTY = "empty"
    PAWN = "pawn"
    ROOK = "rook"
    BISHOP = "bishop"
    QUEEN = "queen"
    KNIGHT = "knight"
    KING = "king"


class Color(Enum):
    NONE = -1
    WHITE = 0
    BLACK = 1


PIECE_STR: dict[PieceType, tuple[str, str]] = {
    PieceType.EMPTY: (" ", " "),
    PieceType.PAWN: ("♙", "♟"),
    PieceType.ROOK: ("♖", "♜"),
    PieceType.BISHOP: ("♗", "♝"),
    PieceType.QUEEN: ("♕", "♛"),
    PieceType.KING: ("♔", "♚"),
    PieceType.KNIGHT: ("♘", "♞"),
}

FEN_MAP: dict[str, PieceType] = {
    "p": PieceType.PAWN,
    "r": PieceType.ROOK,
    "b": PieceType.BISHOP,
    "q": PieceType.QUEEN,
    "k": PieceType.KING,
    "n": PieceType.KNIGHT,
}


@dataclass
class Piece:
    x: int
    y: int
    color: Color = Color.NONE
    type: PieceType = PieceType.EMPTY

    @staticmethod
    def from_fen(x: int, y: int, fen: str) -> Self:
        color = Color.WHITE if fen.isupper() else Color.BLACK
        return Piece(x, y, color, type=FEN_MAP[fen.lower()])

    def promote_to_queen(self) -> None:
        self.type = PieceType.QUEEN

    def __str__(self):
        return PIECE_STR[self.type][self.color.value]


def main() -> None:
    queen = Piece(0, 0, Color.WHITE, PieceType.QUEEN)
    pawn = Piece.from_fen(0, 0, "p")
    print(queen)
    print(pawn)


if __name__ == "__main__":
    main()
