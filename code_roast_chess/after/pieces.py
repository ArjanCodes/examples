from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from enum import Enum


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
    has_moved: bool = False
    moves_made: int = 0
    last_moved: int = 0

    @staticmethod
    def from_fen(x: int, y: int, fen: str) -> Piece:
        color = Color.WHITE if fen.isupper() else Color.BLACK
        return Piece(x, y, color, type=FEN_MAP[fen])

    def move_to(self, x: int, y: int) -> None:
        self.x, self.y = x, y
        self.has_moved = True
        self.moves_made += 1

    def promote_to_queen(self) -> None:
        self.type = PieceType.QUEEN

    @property
    def image(self) -> str:
        return f"pieces/{self.type}{self.color}.png"

    def __str__(self):
        return PIECE_STR[self.type][self.color]


class Pawn(Piece):
    def get_moves(self, board):
        validmoves = []

        if self.color == 1:
            if not self.has_moved:
                if isinstance(board[self.y + 2][self.x], Empty) and isinstance(
                    board[self.y + 1][self.x], Empty
                ):
                    validmoves.append((self.x, self.y + 2))

            if self.y + 1 < 8:
                if isinstance(board[self.y + 1][self.x], Empty):
                    validmoves.append((self.x, self.y + 1))

                if (
                    self.x + 1 < 8
                    and isinstance(board[self.y + 1][self.x + 1], Piece)
                    and not isinstance(board[self.y + 1][self.x + 1], Empty)
                    and board[self.y + 1][self.x + 1].color != self.color
                ):
                    validmoves.append((self.x + 1, self.y + 1))

                if (
                    self.x - 1 >= 0
                    and isinstance(board[self.y + 1][self.x - 1], Piece)
                    and not isinstance(board[self.y + 1][self.x - 1], Empty)
                    and board[self.y + 1][self.x - 1].color != self.color
                ):
                    validmoves.append((self.x - 1, self.y + 1))

            # en passant
            if self.y == 4:
                if (
                    self.x + 1 < 8
                    and isinstance(board[self.y][self.x + 1], Pawn)
                    and board[self.y][self.x + 1].color != self.color
                ):
                    if (
                        board[self.y][self.x + 1].moves_made == 1
                        and board[self.y][self.x + 1].last_moved == -1
                    ):
                        if isinstance(board[self.y + 1][self.x + 1], Empty):
                            validmoves.append((self.x + 1, self.y + 1))

                if (
                    self.x - 1 >= 0
                    and isinstance(board[self.y][self.x - 1], Pawn)
                    and board[self.y][self.x - 1].color != self.color
                ):
                    if (
                        board[self.y][self.x - 1].moves_made == 1
                        and board[self.y][self.x - 1].last_moved == -1
                    ):
                        if isinstance(board[self.y + 1][self.x - 1], Empty):
                            validmoves.append((self.x - 1, self.y + 1))

        else:
            if not self.has_moved:
                if isinstance(board[self.y - 2][self.x], Empty) and isinstance(
                    board[self.y - 1][self.x], Empty
                ):
                    validmoves.append((self.x, self.y - 2))

            if self.y - 1 >= 0:
                if isinstance(board[self.y - 1][self.x], Empty):
                    validmoves.append((self.x, self.y - 1))

                if (
                    self.x + 1 < 8
                    and isinstance(board[self.y - 1][self.x + 1], Piece)
                    and not isinstance(board[self.y - 1][self.x + 1], Empty)
                    and board[self.y - 1][self.x + 1].color != self.color
                ):
                    validmoves.append((self.x + 1, self.y - 1))

                if (
                    self.x - 1 >= 0
                    and isinstance(board[self.y - 1][self.x - 1], Piece)
                    and not isinstance(board[self.y - 1][self.x - 1], Empty)
                    and board[self.y - 1][self.x - 1].color != self.color
                ):
                    validmoves.append((self.x - 1, self.y - 1))

            # en passant
            if self.y == 3:
                if (
                    self.x + 1 < 8
                    and isinstance(board[self.y][self.x + 1], Pawn)
                    and board[self.y][self.x + 1].color != self.color
                ):
                    if (
                        board[self.y][self.x + 1].moves_made == 1
                        and board[self.y][self.x + 1].last_moved == -1
                    ):
                        if isinstance(board[self.y - 1][self.x + 1], Empty):
                            validmoves.append((self.x + 1, self.y - 1))

                if (
                    self.x - 1 >= 0
                    and isinstance(board[self.y][self.x - 1], Pawn)
                    and board[self.y][self.x - 1].color != self.color
                ):
                    if (
                        board[self.y][self.x - 1].moves_made == 1
                        and board[self.y][self.x - 1].last_moved == -1
                    ):
                        if isinstance(board[self.y - 1][self.x - 1], Empty):
                            validmoves.append((self.x - 1, self.y - 1))

        return validmoves


class Rook(Piece):
    def __init__(self, pos: tuple, color: int):
        super().__init__(pos, color)
        self.image = "pieces/rook" + str(self.color) + ".png"

    def get_moves(self, board: list):
        validmoves = []
        for i in range(1, 8 - self.x):
            if isinstance(board[self.y][self.x + i], Empty):
                validmoves.append((self.x + i, self.y))
            elif board[self.y][self.x + i].color != self.color:
                validmoves.append((self.x + i, self.y))
                break
            else:
                break

        for i in range(1, 8 - self.y):
            if isinstance(board[self.y + i][self.x], Empty):
                validmoves.append((self.x, self.y + i))
            elif self.color != board[self.y + i][self.x].color:
                validmoves.append((self.x, self.y + i))
                break
            else:
                break
        for i in range(1, self.x + 1):
            if isinstance(board[self.y][self.x - i], Empty):
                validmoves.append((self.x - i, self.y))
            elif self.color != board[self.y][self.x - i].color:
                validmoves.append((self.x - i, self.y))
                break
            else:
                break

        for i in range(1, self.y + 1):
            if isinstance(board[self.y - i][self.x], Empty):
                validmoves.append((self.x, self.y - i))
            elif self.color != board[self.y - i][self.x].color:
                validmoves.append((self.x, self.y - i))
                break
            else:
                break
        return validmoves


class Bishop(Piece):
    def __init__(self, pos: tuple, color: int):
        super().__init__(pos, color)
        self.image = "pieces/bishop" + str(self.color) + ".png"

    def get_moves(self, board: list):
        validmoves = []
        for x in range(1, 8 - self.x):
            if self.y + x < 8 and self.x + x < 8:
                if isinstance(board[self.y + x][self.x + x], Empty):
                    validmoves.append((self.x + x, self.y + x))
                elif self.color != board[self.y + x][self.x + x].color:
                    validmoves.append((self.x + x, self.y + x))
                    break
                else:
                    break
            else:
                break

        for x in range(1, 8 - self.x):
            if self.y - x >= 0 and self.x + x < 8:
                if isinstance(board[self.y - x][self.x + x], Empty):
                    validmoves.append((self.x + x, self.y - x))
                elif self.color != board[self.y - x][self.x + x].color:
                    validmoves.append((self.x + x, self.y - x))
                    break
                else:
                    break
            else:
                break

        for x in range(1, self.x + 1):
            if self.y + x < 8 and self.x - x >= 0:
                if isinstance(board[self.y + x][self.x - x], Empty):
                    validmoves.append((self.x - x, self.y + x))
                elif (
                    self.y + x < 8 and self.color != board[self.y + x][self.x - x].color
                ):
                    validmoves.append((self.x - x, self.y + x))
                    break
                else:
                    break
            else:
                break

        for x in range(1, self.x + 1):
            if self.y - x >= 0 and self.x - x >= 0:
                if isinstance(board[self.y - x][self.x - x], Empty):
                    validmoves.append((self.x - x, self.y - x))
                elif self.color != board[self.y - x][self.x - x].color:
                    validmoves.append((self.x - x, self.y - x))
                    break
                else:
                    break
            else:
                break

        return validmoves


class Queen(Piece):
    def __init__(self, pos: tuple, color: int):
        super().__init__(pos, color)
        self.image = "pieces/queen" + str(self.color) + ".png"

    def get_moves(self, board: list):
        validmoves = []

        # Diagonal moves
        for x in range(1, 8 - self.x):
            if self.y + x < 8:
                if isinstance(board[self.y + x][self.x + x], Empty):
                    validmoves.append((self.x + x, self.y + x))
                elif self.color != board[self.y + x][self.x + x].color:
                    validmoves.append((self.x + x, self.y + x))
                    break
                else:
                    break
            else:
                break

        for x in range(1, 8 - self.x):
            if self.y - x >= 0:
                if isinstance(board[self.y - x][self.x + x], Empty):
                    validmoves.append((self.x + x, self.y - x))
                elif self.color != board[self.y - x][self.x + x].color:
                    validmoves.append((self.x + x, self.y - x))
                    break
                else:
                    break
            else:
                break

        for x in range(1, self.x + 1):
            if self.y + x < 8:
                if isinstance(board[self.y + x][self.x - x], Empty):
                    validmoves.append((self.x - x, self.y + x))
                elif self.color != board[self.y + x][self.x - x].color:
                    validmoves.append((self.x - x, self.y + x))
                    break
                else:
                    break

        for x in range(1, self.x + 1):
            if self.y - x >= 0:
                if isinstance(board[self.y - x][self.x - x], Empty):
                    validmoves.append((self.x - x, self.y - x))
                elif self.color != board[self.y - x][self.x - x].color:
                    validmoves.append((self.x - x, self.y - x))
                    break
                else:
                    break
            else:
                break

        # Moves on x-axis
        for x in range(1, 8 - self.x):
            if isinstance(board[self.y][self.x + x], Empty):
                validmoves.append((self.x + x, self.y))
            elif self.color != board[self.y][self.x + x].color:
                validmoves.append((self.x + x, self.y))
                break
            else:
                break
        for x in range(1, self.x + 1):
            if isinstance(board[self.y][self.x - x], Empty):
                validmoves.append((self.x - x, self.y))
            elif self.color != board[self.y][self.x - x].color:
                validmoves.append((self.x - x, self.y))
                break
            else:
                break

        # Moves on y-axis
        for y in range(1, 8 - self.y):
            if isinstance(board[self.y + y][self.x], Empty):
                validmoves.append((self.x, self.y + y))
            elif self.color != board[self.y + y][self.x].color:
                validmoves.append((self.x, self.y + y))
                break
            else:
                break
        for y in range(1, self.y + 1):
            if isinstance(board[self.y - y][self.x], Empty):
                validmoves.append((self.x, self.y - y))
            elif self.color != board[self.y - y][self.x].color:
                validmoves.append((self.x, self.y - y))
                break
            else:
                break
        return validmoves


class King(Piece):
    def __init__(self, pos: tuple, color: int):
        super().__init__(pos, color)
        self.image = "pieces/king" + str(self.color) + ".png"

    def is_in_check(self, board: list):
        for x in range(8):
            for y in range(8):
                if (
                    not isinstance(board[y][x], Empty)
                    and not isinstance(board[y][x], King)
                    and board[y][x].color != self.color
                ):
                    if (self.x, self.y) in board[y][x].get_moves(board):
                        return True

        return False

    def check_if_targeting_target(self, target: tuple):
        possible_moves = set(
            (
                (self.x + 1, self.y),
                (self.x - 1, self.y),
                (self.x, self.y + 1),
                (self.x, self.y - 1),
                (self.x + 1, self.y + 1),
                (self.x + 1, self.y - 1),
                (self.x - 1, self.y + 1),
                (self.x - 1, self.y - 1),
            )
        )
        return target in possible_moves

    def check_if_targeted_at_pos(self, board: list, pos: tuple):
        targetx, targety = pos

        tempboard = deepcopy(board)
        tempboard[targety][targetx] = tempboard[self.y][self.x]
        tempboard[self.y][self.x] = Empty()
        for row in tempboard:
            for piece in row:
                if not isinstance(piece, Empty) and piece.color != self.color:
                    if isinstance(piece, King):
                        if piece.check_if_targeting_target((targetx, targety)):
                            return True
                    else:
                        if pos in piece.get_moves(tempboard):
                            return True
        return False

    def get_moves(self, board: list):
        validmoves = []
        possible_moves = (
            (self.x + 1, self.y),
            (self.x - 1, self.y),
            (self.x, self.y + 1),
            (self.x, self.y - 1),
            (self.x + 1, self.y + 1),
            (self.x + 1, self.y - 1),
            (self.x - 1, self.y + 1),
            (self.x - 1, self.y - 1),
        )
        for e in possible_moves:
            x, y = e
            if 0 <= x <= 7 and 0 <= y <= 7:
                if isinstance(board[y][x], Empty) or self.color != board[y][x].color:
                    if not self.check_if_targeted_at_pos(board, e):
                        validmoves.append(e)
        return validmoves


class Knight(Piece):
    def __init__(self, pos: tuple, color: int):
        super().__init__(pos, color)
        self.image = "pieces/knight" + str(self.color) + ".png"

    def get_moves(self, board: list):
        validmoves = []
        moves = (
            (self.x + 1, self.y + 2),
            (self.x + 1, self.y - 2),
            (self.x - 1, self.y + 2),
            (self.x - 1, self.y - 2),
            (self.x + 2, self.y + 1),
            (self.x + 2, self.y - 1),
            (self.x - 2, self.y + 1),
            (self.x - 2, self.y - 1),
        )
        for e in moves:
            x, y = e
            if 0 <= x <= 7 and 0 <= y <= 7:
                if isinstance(board[y][x], Empty) or self.color != board[y][x].color:
                    validmoves.append(e)
        return validmoves
