from tkinter import *
from logic import ChessLogic
from pieces import *

# (⌐■_■)#


class GUI(Frame):
    def __init__(
        self, master, size=85, color1="#eeeed2", color2="#769656"
    ):
        self.rows = 8
        self.columns = 8
        self.size = size
        self.color1 = color1
        self.color2 = color2
  
        self.game = ChessLogic()
        self.board = self.game.board

        Frame.__init__(self, borderwidth=5) 

        self.init_game()
        self.make_window()
        self.draw_board()

    def init_game(self):
        self.game.reset_game()
        self.game.populateWithFen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
        self.squareButton = {}
        self.images = {}
        self.colorAtSquare = {}
        self.squareNoAtPos = {}
        self.squares = []
        self.pieceTo = [(-1, -1)] * 2

    def clearWindow(self):
        for widget in self.top.winfo_children():
            widget.destroy()

    def colorAllSquares(self):
        colornumber = 0
        for row in range(self.rows):
            colornumber += 1
            for col in range(self.columns):
                if (colornumber % 2) == 0:
                    color = self.color2
                else:
                    color = self.color1
                self.squareButton[self.squareNoAtPos[(col, row)]].configure(bg=color)
                colornumber += 1

    def commandHandler(self, pos: tuple):

        x, y = pos


        self.colorAllSquares()

        # Rokade
        if isinstance(self.board[self.pieceTo[0][1]][self.pieceTo[0][0]], King):
            if (isinstance(self.board[y][x], Rook) and self.board[y][x].color == self.game.player_turn):
                
                self.pieceTo[1] = pos

                if x == 0:
                    self.pieceTo.append((x + 2, y))
                    self.pieceTo.append((x + 3, y))
                elif x == 7:
                    self.pieceTo.append((x - 1, y))
                    self.pieceTo.append((x - 2, y))

                self.game.move_piece(self.pieceTo[0], pos)
                self.refresh(self.pieceTo)


        if self.game.player_turn == self.board[y][x].color:
            # color the squares that the piece can move to

            for move in self.board[y][x].get_moves(self.board):
                self.squareButton[self.squareNoAtPos[move]].configure(bg="gray")

            self.pieceTo[0] = pos
        elif isinstance(self.board[self.pieceTo[0][1]][self.pieceTo[0][0]].get_moves(self.board), list):
            if pos in self.board[self.pieceTo[0][1]][self.pieceTo[0][0]].get_moves(self.board) and self.pieceTo[0] != (-1, -1):
                self.pieceTo[1] = pos

                #En passant
                if isinstance(self.board[self.pieceTo[0][1]][self.pieceTo[0][0]], Pawn) and isinstance(self.board[y][x], Empty) and x != self.pieceTo[0][0]:
                    self.pieceTo.append((x, self.pieceTo[0][1]))

                self.game.move_piece(self.pieceTo[0], self.pieceTo[1])
                self.refresh(self.pieceTo)

    def make_window(self):
        self.top = self.winfo_toplevel()
        self.top.resizable(False, False)

    def get_top_pos(self):
        return self.top.winfo_x(), self.top.winfo_y()

    def draw_board(self):
        self.clearWindow()
        squarenumber = 0
        colornumber = 0
        for row in range(self.rows):
            colornumber += 1
            for col in range(self.columns):
                if (colornumber % 2) == 0:
                    color = self.color2
                else:
                    color = self.color1
                self.images[squarenumber] = PhotoImage(file=self.game.board[row][col].image).subsample(2, 2)
                self.squareButton[squarenumber] = Button(
                    self.top,
                    command=(
                        lambda pos=(col, row): self.commandHandler(pos)
                    ),
                    width=self.size,
                    height=self.size,
                    bg=color,
                    image=self.images[squarenumber],
                )
                self.squareButton[squarenumber].grid(
                    row=row, column=col, sticky=N + S + E + W
                )
                self.colorAtSquare[squarenumber] = color
                self.squareNoAtPos[(col, row)] = squarenumber

                squarenumber += 1
                colornumber += 1

    def newgame(self):
        self.game.STATUS = 1
        self.init_game()
        self.draw_board()
        self.top.attributes("-disabled", False)

    def endscreen(self):
        self.endwindow = Toplevel(root)
        self.endwindow.title("GAME OVER")
        endwindow_pos_x = self.get_top_pos()[0] + self.top.winfo_width()
        endwindow_pos_y = self.get_top_pos()[1]
        self.endwindow.geometry(f"250x100+{endwindow_pos_x}+{endwindow_pos_y}")

        if self.game.STATUS == 3:
            winner = "White wins!"
        elif self.game.STATUS == 2:
            winner = "Black wins!"

        self.winnerlabel = Label(self.endwindow, text=winner).pack()
        self.retrybut = Button(
            self.endwindow, text="retry", command=self.newgame
        ).pack()

        self.top.attributes("-disabled", True, "-topmost", True)

    def refresh(self, pos: list):
        for p in pos:
            squareNo = self.squareNoAtPos[p]
            x, y = p
            self.images[squareNo] = PhotoImage(file=self.game.board[y][x].image).subsample(2, 2)

            self.squareButton[squareNo] = Button(self.top,
                command=(lambda pos=(x, y): self.commandHandler(pos)),
                width=self.size,
                height=self.size,
                bg=self.colorAtSquare[squareNo],
                image=self.images[squareNo],)
            self.squareButton[squareNo].grid(row=y, column=x, sticky=N + S + E + W)

        self.pieceTo = [(-1, -1)] * 2

        if self.game.STATUS != 1:
            self.endscreen()


if __name__ == "__main__":
    root = Tk()
    game = GUI(root)
    game.master.title("Chess")
    root.mainloop()
