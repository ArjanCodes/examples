from copy import deepcopy

from board import Board
from pieces import *


class ChessLogic:
    def __init__(self):
        self.board = Board()
        # player_turn bestemmer hvilken spillerens tur det er: 0 for hvid og 1 for sort
        self.player_turn = Color.WHITE
        # Status bestemmer om der er en runde i gang:
        # 1 for i gang, 3 for spillet er over og hvide brikker har vundet og 2 for sorte brikker har vundet
        self.status = 1
        self.current_move_no = 0

    def reset_game(self):
        self.player_turn = 0

    def populate_with_fen(self, fen: str):

        # fenlist er en liste af strings, hver string er en linje i fen-notationen
        fenlist = fen.split("/")

        for indy, y in enumerate(fenlist):
            extra = 0
            for indx, x in enumerate(y):
                if x.isnumeric():
                    for i in range(int(x)):
                        if i > 0:
                            extra += 1
                        self.board.place(Piece(indx + extra, indy))
                else:
                    self.board.place(Piece.from_fen(indx + extra, indy, x))

    def update_pawn_currentMoveNo(self):
        for x in self.board:
            for y in x:
                if isinstance(y, Pawn):
                    y.currentMoveNo = self.current_move_no

    def move_piece(self, piece: tuple, newpos: tuple):
        x, y = piece
        newx, newy = newpos

        # Hvis det ikke er en konge og den nye position ikke er i check, flyt brikken
        if (
            newpos in self.board[y][x].get_moves(self.board)
            and not isinstance(self.board[y][x], King)
            and not isinstance(self.board[y][x], Empty)
        ):

            king = self.board.find_king(self.player_turn)
            tempboard = deepcopy(self.board)
            tempboard[newy][newx] = tempboard[y][x]
            tempboard[y][x] = Empty()

            if not tempboard[kingposy][kingposx].is_in_check(tempboard):
                # Hvis brikken er en pawn og den kan blive promoveret, så skal den blive promoveret
                if isinstance(self.board[y][x], Pawn):
                    if self.board[y][x].color == 0 and newy == 0:
                        self.promote_to_queen(self.board[y][x])
                    elif self.board[y][x].color == 1 and newy == 7:
                        self.promote_to_queen(self.board[y][x])

                # Opdaterer brikkens position
                # En passant
                if (
                    isinstance(self.board[y][x], Pawn)
                    and isinstance(self.board[newy][newx], Empty)
                    and newx != x
                ):
                    # if (newx == x + 1 and newy == y + 1) or (newx == x - 1 and newy == y + 1) or (newx == x + 1 and newy == y - 1) or (newx == x - 1 and newy == y - 1):
                    self.board[newy][newx] = self.board[y][x]
                    self.board[y][x] = Empty()
                    self.board[y][newx] = Empty()
                    # else: self.board[y][x+newx] = Empty()
                    self.board[newy][newx].move((newx, newy))
                    self.board[newy][newx].last_moved = self.current_move_no
                    self.player_turn = 1 if self.player_turn == 0 else 0
                    self.current_move_no += 1
                    self.update_pawn_currentMoveNo()

                # Normalt
                else:
                    self.board[newy][newx] = self.board[y][x]
                    self.board[y][x] = Empty()
                    self.board[newy][newx].move((newx, newy))
                    self.board[newy][newx].last_moved = self.current_move_no
                    self.player_turn = 1 if self.player_turn == 0 else 0
                    self.current_move_no += 1
                    self.update_pawn_currentMoveNo()

        # Hvis det er en konge og den nye position er valid, flyt brikken
        elif isinstance(self.board[y][x], King) and newpos in self.board[y][
            x
        ].get_moves(self.board):
            self.board[newy][newx] = self.board[y][x]
            self.board[y][x] = Empty()
            self.board[newy][newx].move((newx, newy))
            self.board[newy][newx].last_moved = self.current_move_no
            self.player_turn = 1 if self.player_turn == 0 else 0
            self.current_move_no += 1
            self.update_pawn_currentMoveNo()

        # Rokade
        elif (
            isinstance(self.board[y][x], King)
            and not self.board[y][x].has_moved
            and not self.board[y][x].is_in_check(self.board)
            and isinstance(self.board[newy][newx], Rook)
            and not self.board[newy][newx].has_moved
        ):

            # Tjek om rokaden er muligt ved at tjekke om det er en brikke mellem kongen og tårnet til venstre
            left = False
            if newx == 0:
                left = True
                for i in range(1, 4):
                    if not isinstance(self.board[y][x - i], Empty):
                        return
            elif newx == 7:
                left = False
                for i in range(1, 3):
                    if not isinstance(self.board[y][x + i], Empty):
                        return

            kingmove = (x - 2, y) if left else (x + 2, y)
            rookmove = (newx + 3, newy) if left else (newx - 2, newy)

            # Tjek om kongen kommer i skak
            tempboard = deepcopy(self.board)
            # Flyt tårnet 3 pladser til højre hvis venstre, ellers 2 pladser til venstre
            tempboard[newy][newx].move(rookmove)
            tempboard[newy][rookmove[0]] = tempboard[newy][newx]
            tempboard[newy][newx] = Empty()
            # Flyt kongen 2 pladser til venstre hvis venstre, ellers 2 til højre
            tempboard[y][x].move(kingmove)
            tempboard[y][kingmove[0]] = tempboard[y][x]
            tempboard[y][x] = Empty()

            if not tempboard[y][kingmove[0]].is_in_check(tempboard):
                # Flyt det venstre tårn 3 pladser til højre
                self.board[newy][newx].move(rookmove)
                self.board[newy][rookmove[0]] = self.board[newy][newx]
                self.board[newy][newx] = Empty()

                # Flyt kongen 2 pladser til venstre
                self.board[y][x].move(kingmove)
                self.board[y][kingmove[0]] = self.board[y][x]
                self.board[y][x] = Empty()
                self.board[newy][newx].last_moved = self.current_move_no
                self.player_turn = 1 if self.player_turn == 0 else 0
                self.current_move_no += 1
                self.update_pawn_currentMoveNo()

        if self.check_for_check():
            if self.check_for_mate():
                self.status = 2 if self.player_turn == 0 else 3

    def find_the_king(self):
        for row in self.board:
            for piece in row:
                if isinstance(piece, King) and piece.color == self.player_turn:
                    return (piece.x, piece.y)

    def check_for_check(self):
        for x in self.board:
            for y in x:
                if isinstance(y, King) and y.color == self.player_turn:
                    if y.is_in_check(self.board):
                        return True
        return False

    def check_for_mate(self):

        kingposx, kingposy = self.find_the_king()
        for x in self.board:
            for y in x:
                if y.color == self.player_turn:
                    if isinstance(y, King) and y.get_moves(self.board):
                        return False
                    elif not isinstance(y, King):
                        for move in y.get_moves(self.board):
                            xmove, ymove = move
                            tempboard = deepcopy(self.board)
                            tempboard[ymove][xmove] = tempboard[y.y][y.x]
                            tempboard[y.y][y.x] = Empty()
                            if not tempboard[kingposy][kingposx].is_in_check(tempboard):
                                return False
        return True
