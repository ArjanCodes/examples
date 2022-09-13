from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from moves import Position, get_valid_moves_rook
from pieces import Color, Piece, PieceType

Grid = dict[Position, Piece]


def empty_board() -> Grid:
    grid: Grid = {}
    for x in range(8):
        for y in range(8):
            grid[(x, y)] = Piece(x, y)
    return grid


@dataclass
class Board:
    pieces: Grid = field(default_factory=empty_board)

    @staticmethod
    def from_fen(fen: str) -> Board:
        board = Board()
        fenlist = fen.split("/")

        for indy, y in enumerate(fenlist):
            extra = 0
            for indx, x in enumerate(y):
                if x.isnumeric():
                    for i in range(int(x)):
                        if i > 0:
                            extra += 1
                        board.place(Piece(indx + extra, indy))
                else:
                    board.place(Piece.from_fen(indx + extra, indy, x))
        return board

    def place(self, piece: Piece) -> None:
        self.pieces[(piece.x, piece.y)] = Piece

    def piece(self, x: int, y: int) -> Piece:
        return self.pieces[(x, y)]

    def empty(self, x: int, y: int) -> bool:
        return self.piece(x, y).type == PieceType.EMPTY

    def find_king(self, color: Color) -> Piece:
        for piece in self.pieces.values():
            if piece.type == PieceType.KING and color == piece.color:
                return piece

    def get_valid_moves(self, x: int, y: int) -> list[Position]:
        return MOVE_LISTS[self.piece(x, y)]


ValidMoveCalculator = Callable[[Board, int, int], list[Position]]


MOVE_LISTS: dict[PieceType, ValidMoveCalculator] = {
    PieceType.ROOK: get_valid_moves_rook
}
