import tkinter as tk

import pieces
from logic import ChessLogic

# (⌐■_■)#


class GUI(tk.Frame):
    def __init__(
        self,
        master: tk.Tk,
        size: int = 85,
        color1: str = "#ababd2",
        color2: str = "#123456",
    ) -> None:
        self.rows = 8
        self.columns = 8
        self.size = size
        self.color1 = color1
        self.color2 = color2

        self.game = ChessLogic()
        self.board = self.game.board

        super().__init__(borderwidth=5, master=master)

        self.init_game()
        self.make_window()
        self.draw_board()

    def init_game(self) -> None:
        self.game.reset_game()
        self.game.populateWithFen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
        self.square_button: dict[int, tk.Button] = {}
        self.images = {}
        self.color_at_square = {}
        self.square_no_at_pos = {}
        self.squares = []
        self.piece_to = [(-1, -1)] * 2

    def clear_window(self) -> None:
        for widget in self.top.winfo_children():
            widget.destroy()

    def color_all_squares(self) -> None:
        colornumber = 0
        for row in range(self.rows):
            colornumber += 1
            for col in range(self.columns):
                if (colornumber % 2) == 0:
                    color = self.color2
                else:
                    color = self.color1
                self.square_button[self.square_no_at_pos[(col, row)]].configure(
                    bg=color
                )
                colornumber += 1

    def command_handler(self, pos: tuple):

        x, y = pos

        self.color_all_squares()

        # Rokade
        if isinstance(
            self.board[self.piece_to[0][1]][self.piece_to[0][0]], pieces.King
        ):
            if (
                isinstance(self.board[y][x], pieces.Rook)
                and self.board[y][x].color == self.game.player_turn
            ):

                self.piece_to[1] = pos

                if x == 0:
                    self.piece_to.append((x + 2, y))
                    self.piece_to.append((x + 3, y))
                elif x == 7:
                    self.piece_to.append((x - 1, y))
                    self.piece_to.append((x - 2, y))

                self.game.move_piece(self.piece_to[0], pos)
                self.refresh(self.piece_to)

        if self.game.player_turn == self.board[y][x].color:
            # color the squares that the piece can move to

            for move in self.board[y][x].get_moves(self.board):
                self.square_button[self.square_no_at_pos[move]].configure(bg="gray")

            self.piece_to[0] = pos
        elif isinstance(
            self.board[self.piece_to[0][1]][self.piece_to[0][0]].get_moves(self.board),
            list,
        ):
            if pos in self.board[self.piece_to[0][1]][self.piece_to[0][0]].get_moves(
                self.board
            ) and self.piece_to[0] != (-1, -1):
                self.piece_to[1] = pos

                # En passant
                if (
                    isinstance(
                        self.board[self.piece_to[0][1]][self.piece_to[0][0]],
                        pieces.Pawn,
                    )
                    and isinstance(self.board[y][x], pieces.Empty)
                    and x != self.piece_to[0][0]
                ):
                    self.piece_to.append((x, self.piece_to[0][1]))

                self.game.move_piece(self.piece_to[0], self.piece_to[1])
                self.refresh(self.piece_to)

    def make_window(self):
        self.top = self.winfo_toplevel()
        self.top.resizable(False, False)

    def get_top_pos(self):
        return self.top.winfo_x(), self.top.winfo_y()

    def draw_board(self):
        self.clear_window()
        squarenumber = 0
        colornumber = 0
        for row in range(self.rows):
            colornumber += 1
            for col in range(self.columns):
                if (colornumber % 2) == 0:
                    color = self.color2
                else:
                    color = self.color1
                self.images[squarenumber] = tk.PhotoImage(
                    file=self.game.board[row][col].image
                ).subsample(2, 2)
                self.square_button[squarenumber] = tk.Button(
                    self.top,
                    command=(lambda pos=(col, row): self.command_handler(pos)),
                    width=self.size,
                    height=self.size,
                    bg=color,
                    image=self.images[squarenumber],
                )
                self.square_button[squarenumber].grid(
                    row=row, column=col, sticky=tk.N + tk.S + tk.E + tk.W
                )
                self.color_at_square[squarenumber] = color
                self.square_no_at_pos[(col, row)] = squarenumber

                squarenumber += 1
                colornumber += 1

    def newgame(self):
        self.game.STATUS = 1
        self.init_game()
        self.draw_board()
        self.top.attributes("-disabled", False)

    def endscreen(self):
        self.endwindow = tk.Toplevel(self.master)
        self.endwindow.title("GAME OVER")
        endwindow_pos_x = self.get_top_pos()[0] + self.top.winfo_width()
        endwindow_pos_y = self.get_top_pos()[1]
        self.endwindow.geometry(f"250x100+{endwindow_pos_x}+{endwindow_pos_y}")

        if self.game.STATUS == 3:
            winner = "White wins!"
        elif self.game.STATUS == 2:
            winner = "Black wins!"

        winner_label = tk.Label(self.endwindow, text=winner)
        retry_button = tk.Button(self.endwindow, text="retry", command=self.newgame)
        winner_label.pack()
        retry_button.pack()

        self.top.attributes("-disabled", True, "-topmost", True)

    def refresh(self, pos: list):
        for p in pos:
            square_no = self.square_no_at_pos[p]
            x, y = p
            self.images[square_no] = tk.PhotoImage(
                file=self.game.board[y][x].image
            ).subsample(2, 2)

            self.square_button[square_no] = tk.Button(
                self.top,
                command=(lambda pos=(x, y): self.command_handler(pos)),
                width=self.size,
                height=self.size,
                bg=self.color_at_square[square_no],
                image=self.images[square_no],
            )
            self.square_button[square_no].grid(
                row=y, column=x, sticky=tk.N + tk.S + tk.E + tk.W
            )

        self.piece_to = [(-1, -1)] * 2

        if self.game.STATUS != 1:
            self.endscreen()


def main() -> None:
    master = tk.Tk()
    master.title("Chess")
    game = GUI(master)
    game.mainloop()


# root.mainloop()


if __name__ == "__main__":
    main()
