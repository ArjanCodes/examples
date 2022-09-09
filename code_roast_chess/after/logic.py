from pieces import *
from copy import deepcopy

class ChessLogic:
    def __init__(self):
        self.board = [[Empty() for x in range(8)] for y in range(8)]
        # player_turn bestemmer hvilken spillerens tur det er: 0 for hvid og 1 for sort
        self.player_turn = 0
        # Status bestemmer om der er en runde i gang:
        # 1 for i gang, 3 for spillet er over og hvide brikker har vundet og 2 for sorte brikker har vundet
        self.STATUS = 1
        self.currentMoveNo = 0

    def reset_game(self):
        self.player_turn = 0

    def populateWithFen(self, fen: str):

        #fenlist er en liste af strings, hver string er en linje i fen-notationen
        fenlist = fen.split("/")
        
        for indy, y in enumerate(fenlist):
            extra = 0
            for indx, x in enumerate(y):
                if x == "r":
                    self.board[indy][indx + extra] = Rook((indx + extra, indy), 1)
                elif x == "n":
                    self.board[indy][indx + extra] = Knight((indx + extra, indy), 1)
                elif x == "b":
                    self.board[indy][indx + extra] = Bishop((indx + extra, indy), 1)
                elif x == "q":
                    self.board[indy][indx + extra] = Queen((indx + extra, indy), 1)
                elif x == "k":
                    self.board[indy][indx + extra] = King((indx + extra, indy), 1)
                elif x == "p":
                    self.board[indy][indx + extra] = Pawn((indx + extra, indy), 1)
                
                elif x.isnumeric():
                    for i in range(int(x)):
                        if i > 0: extra += 1
                        self.board[indy][indx + extra] = Empty()
                        
                elif x == "R":
                    self.board[indy][indx + extra] = Rook((indx + extra, indy), 0)
                elif x == "N":
                    self.board[indy][indx + extra] = Knight((indx + extra, indy), 0)
                elif x == "B":
                    self.board[indy][indx + extra] = Bishop((indx + extra, indy), 0)
                elif x == "Q":
                    self.board[indy][indx + extra] = Queen((indx + extra, indy), 0)
                elif x == "K":
                    self.board[indy][indx + extra] = King((indx + extra, indy), 0)
                elif x == "P":
                    self.board[indy][indx + extra] = Pawn((indx + extra, indy), 0)

    def update_pawn_currentMoveNo(self):
        for x in self.board:
            for y in x:
                if isinstance(y, Pawn):
                    y.currentMoveNo = self.currentMoveNo

    def move_piece(self, piece: tuple, newpos: tuple):
        x, y = piece
        newx, newy = newpos

        # Hvis det ikke er en konge og den nye position ikke er i check, flyt brikken
        if (newpos in self.board[y][x].get_moves(self.board)
            and not isinstance(self.board[y][x], King)
            and not isinstance(self.board[y][x], Empty)):

            kingposx, kingposy = self.find_the_king()
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
                #En passant
                if isinstance(self.board[y][x], Pawn) and isinstance(self.board[newy][newx], Empty) and newx != x:
                   # if (newx == x + 1 and newy == y + 1) or (newx == x - 1 and newy == y + 1) or (newx == x + 1 and newy == y - 1) or (newx == x - 1 and newy == y - 1):
                    self.board[newy][newx] = self.board[y][x]
                    self.board[y][x] = Empty()
                    self.board[y][newx] = Empty() 
                    # else: self.board[y][x+newx] = Empty()
                    self.board[newy][newx].move((newx, newy))
                    self.board[newy][newx].last_moved = self.currentMoveNo
                    self.player_turn = 1 if self.player_turn == 0 else 0
                    self.currentMoveNo += 1
                    self.update_pawn_currentMoveNo()           
                    

                #Normalt
                else:
                    self.board[newy][newx] = self.board[y][x]
                    self.board[y][x] = Empty()
                    self.board[newy][newx].move((newx, newy))
                    self.board[newy][newx].last_moved = self.currentMoveNo
                    self.player_turn = 1 if self.player_turn == 0 else 0
                    self.currentMoveNo += 1
                    self.update_pawn_currentMoveNo()

        # Hvis det er en konge og den nye position er valid, flyt brikken
        elif isinstance(self.board[y][x], King) and newpos in self.board[y][
            x
        ].get_moves(self.board):
            self.board[newy][newx] = self.board[y][x]
            self.board[y][x] = Empty()
            self.board[newy][newx].move((newx, newy))
            self.board[newy][newx].last_moved = self.currentMoveNo
            self.player_turn = 1 if self.player_turn == 0 else 0
            self.currentMoveNo += 1
            self.update_pawn_currentMoveNo()


        # Rokade
        elif (isinstance(self.board[y][x], King)
            and not self.board[y][x].has_moved
            and not self.board[y][x].is_in_check(self.board)
            and isinstance(self.board[newy][newx], Rook)
            and not self.board[newy][newx].has_moved):

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
                self.board[newy][newx].last_moved = self.currentMoveNo
                self.player_turn = 1 if self.player_turn == 0 else 0
                self.currentMoveNo += 1
                self.update_pawn_currentMoveNo()


        if self.check_for_check():
            if self.check_for_mate():
                self.STATUS = 2 if self.player_turn == 0 else 3

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

    def promote_to_queen(self, piece: Pawn):
        self.board[piece.y][piece.x] = Queen(piece.pos, piece.color)