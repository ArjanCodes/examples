from dataclasses import dataclass, field
from typing import Callable

from .pieces import Color, Piece, PieceType

Position = tuple[int, int]
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


def get_valid_moves_rook(board: Board, x: int, y: int) -> list[Position]:
    validmoves: list[Position] = []
    for i in range(1, 8 - x):
        if board.empty(x + i, y):
            validmoves.append((x + i, y))
        elif board.piece(x + i, y).color != board.piece(x, y).color:
            validmoves.append((x + i, y))
            break
        else:
            break

    for i in range(1, 8 - y):
        if board.empty(x, y + i):
            validmoves.append((x, y + i))
        elif board.piece(x, y).color != board(x, y + i).color:
            validmoves.append((x, y + i))
            break
        else:
            break

    for i in range(1, x + 1):
        if board.empty(x - i, y):
            validmoves.append((x - i, y))
        elif board.piece(x, y).color != board.piece(y, x - i).color:
            validmoves.append((x - i, y))
            break
        else:
            break

    for i in range(1, y + 1):
        if board.empty(x, y - i):
            validmoves.append((x, y - i))
        elif board.piece(x, y).color != board.piece(x, y - i).color:
            validmoves.append((x, y - i))
            break
        else:
            break
    return validmoves


MOVE_LISTS: dict[PieceType, ValidMoveCalculator] = {
    PieceType.ROOK: get_valid_moves_rook
}
