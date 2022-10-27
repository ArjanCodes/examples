from abc import ABC, abstractmethod
from copy import deepcopy


class Piece(ABC):
    def __init__(self, pos: tuple, color: int):
        self.pos = pos
        self.x, self.y = pos
        if self.x < 0 or self.x > 7 or self.y < 0 or self.y > 7:
            raise ValueError("Invalid position")

        # color: -1 for empty, 0 for hvid, 1 for sort
        availablecolors = [-1, 0, 1]
        self.color = color
        if self.color not in availablecolors:
            raise ValueError("Invalid color, use 0 for white and 1 for black")
        self.has_moved = False
        self.moves_made = 0
        self.last_moved = 0
        self.image = ""
        
    @abstractmethod
    def get_moves(self, board: list):
        pass

    def move(self, newpos: tuple):
        self.pos = newpos
        self.x, self.y = newpos
        self.has_moved = True
        self.moves_made += 1

class Empty(Piece):
    def __init__(self, pos=(0, 0), color=-1):
        super().__init__(pos, color)


    def get_moves(self, board: list):
        pass

    def __str__(self):
        return " "


class Pawn(Piece):
    def __init__(self, pos: tuple, color: int):
        super().__init__(pos, color)
        self.image = "pieces/pawn" + str(self.color) + ".png"
        self.currentMoveNo = 0


    def setCurrentMoveNo(self, moveNo):
        self.currentMoveNo = moveNo


    def get_moves(self, board):
        validmoves = []

        if self.color == 1:
            if not self.has_moved:
                if isinstance(board[self.y + 2][self.x], Empty) and isinstance(
                        board[self.y + 1][self.x], Empty):
                    validmoves.append((self.x, self.y + 2))

            if self.y + 1 < 8:
                if isinstance(board[self.y + 1][self.x], Empty):
                    validmoves.append((self.x, self.y + 1))

                if (self.x + 1 < 8
                    and isinstance(board[self.y + 1][self.x + 1], Piece)
                    and not isinstance(board[self.y + 1][self.x + 1], Empty)
                        and board[self.y + 1][self.x + 1].color != self.color):
                    validmoves.append((self.x + 1, self.y + 1))

                if (self.x - 1 >= 0
                    and isinstance(board[self.y + 1][self.x - 1], Piece)
                    and not isinstance(board[self.y + 1][self.x - 1], Empty)
                        and board[self.y + 1][self.x - 1].color != self.color):
                    validmoves.append((self.x - 1, self.y + 1))
            
            #en passant
            if self.y == 4:
                if self.x + 1 < 8 and isinstance(board[self.y][self.x + 1], Pawn) and board[self.y][self.x + 1].color != self.color:
                    if board[self.y][self.x + 1].moves_made == 1 and board[self.y][self.x + 1].last_moved == self.currentMoveNo - 1:
                        if isinstance(board[self.y + 1][self.x + 1], Empty):
                            validmoves.append((self.x + 1, self.y + 1))

                if self.x - 1 >= 0 and isinstance(board[self.y][self.x - 1], Pawn) and board[self.y][self.x - 1].color != self.color:
                    if board[self.y][self.x - 1].moves_made == 1 and board[self.y][self.x - 1].last_moved == self.currentMoveNo - 1:
                        if isinstance(board[self.y + 1][self.x - 1], Empty):
                            validmoves.append((self.x - 1, self.y + 1))

        else:
            if not self.has_moved:
                if isinstance(board[self.y - 2][self.x], Empty) and isinstance(
                    board[self.y - 1][self.x], Empty):
                    validmoves.append((self.x, self.y - 2))

            if self.y - 1 >= 0:
                if isinstance(board[self.y - 1][self.x], Empty):
                    validmoves.append((self.x, self.y - 1))

                if (self.x + 1 < 8
                    and isinstance(board[self.y - 1][self.x + 1], Piece)
                    and not isinstance(board[self.y - 1][self.x + 1], Empty)
                    and board[self.y - 1][self.x + 1].color != self.color):
                    validmoves.append((self.x + 1, self.y - 1))

                if (self.x - 1 >= 0
                    and isinstance(board[self.y - 1][self.x - 1], Piece)
                    and not isinstance(board[self.y - 1][self.x - 1], Empty)
                    and board[self.y - 1][self.x - 1].color != self.color):
                    validmoves.append((self.x - 1, self.y - 1))
                
            #en passant
            if self.y == 3:
                if self.x + 1 < 8 and isinstance(board[self.y][self.x + 1], Pawn) and board[self.y][self.x + 1].color != self.color:
                    if board[self.y][self.x + 1].moves_made == 1 and board[self.y][self.x + 1].last_moved == self.currentMoveNo - 1:
                        if isinstance(board[self.y - 1][self.x + 1], Empty):
                            validmoves.append((self.x + 1, self.y - 1))

                if self.x - 1 >= 0 and isinstance(board[self.y][self.x - 1], Pawn) and board[self.y][self.x - 1].color != self.color:
                    if board[self.y][self.x - 1].moves_made == 1 and board[self.y][self.x - 1].last_moved == self.currentMoveNo - 1:
                        if isinstance(board[self.y - 1][self.x - 1], Empty):
                            validmoves.append((self.x - 1, self.y - 1))

        return validmoves

    def __str__(self):
        return "♙" if self.color == 0 else "♟"


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

    def __str__(self):
        return "♖" if self.color == 0 else "♜"


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
                    self.y +
                        x < 8 and self.color != board[self.y +
                                                      x][self.x - x].color
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

    def __str__(self):
        return "♗" if self.color == 0 else "♝"


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

    def __str__(self):
        return "♕" if self.color == 0 else "♛"


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

    def __str__(self):
        return "♔" if self.color == 0 else "♚"


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

    def __str__(self):
        return "♘" if self.color == 0 else "♞"
