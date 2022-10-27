from typing import Protocol

from pieces import Piece

Position = tuple[int, int]


class Board(Protocol):
    def empty(self, x: int, y: int) -> bool:
        """Whether the field (x, y) is empty."""

    def piece(self, x: int, y: int) -> Piece:
        """Returns the piece at position (x, y)."""


def get_valid_moves_rook(board: Board, x: int, y: int) -> list[Position]:
    valid_moves: list[Position] = []
    for i in range(1, 8 - x):
        if board.empty(x + i, y):
            valid_moves.append((x + i, y))
        elif board.piece(x + i, y).color != board.piece(x, y).color:
            valid_moves.append((x + i, y))
            break
        else:
            break

    for i in range(1, 8 - y):
        if board.empty(x, y + i):
            valid_moves.append((x, y + i))
        elif board.piece(x, y).color != board(x, y + i).color:
            valid_moves.append((x, y + i))
            break
        else:
            break

    for i in range(1, x + 1):
        if board.empty(x - i, y):
            valid_moves.append((x - i, y))
        elif board.piece(x, y).color != board.piece(y, x - i).color:
            valid_moves.append((x - i, y))
            break
        else:
            break

    for i in range(1, y + 1):
        if board.empty(x, y - i):
            valid_moves.append((x, y - i))
        elif board.piece(x, y).color != board.piece(x, y - i).color:
            valid_moves.append((x, y - i))
            break
        else:
            break
    return valid_moves
