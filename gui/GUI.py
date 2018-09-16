import tkinter


# Gomoku simple GUI by Conway v1.0

class Board(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.master_ = master
        self.init_window()
        self.board_canvas = tkinter.Canvas(master, width=620, height=620, bg='sandy brown')
        self.player_1_color = 'black'
        self.player_2_color = 'white'

        # draw lines
        for i in range(15):
            self.board_canvas.create_line(30, 30 + 40 * i, 590, 30 + 40 * i, width=3)
            self.board_canvas.create_line(30 + 40 * i, 30, 30 + 40 * i, 590, width=3)
            self.board_canvas.create_text(30 + 40 * i, 30, font=('consolas bold', 18), text=str(i), fill='white')
            self.board_canvas.create_text(30, 30 + 40 * i, font=('consolas bold', 18), text=str(i), fill='white')

        self.board_canvas.pack()

    def init_window(self):
        self.master.title('GUI')
        self.pack(fill=tkinter.BOTH, expand=True)

    # chess piece size r = 15, one square side = 20
    # to draw a piece: up left x = 15 + 40*(x_cords - 1), y = 15 + 40*(y_cords - 1)
    #                  down right x = 45 + 40*(x_cords - 1), y = 45 + 40*(y_cords - 1)
    def draw_piece(self, x_cords, y_cords, color):
        self.board_canvas.create_oval(15 + 40 * (y_cords - 1), 15 + 40 * (x_cords - 1), 45 + 40 * (y_cords - 1),
                                      45 + 40 * (x_cords - 1), fill=color, width=2, tags='pieces')

    def redraw_board(self, state):
        # clear prev state
        self.board_canvas.delete('pieces')
        # draw new state
        for row in range(15):
            for col in range(15):
                if state[row][col] == 1:
                    self.draw_piece(row + 1, col + 1, self.player_1_color)
                elif state[row][col] == 2:
                    self.draw_piece(row + 1, col + 1, self.player_2_color)


def display(state):
    app.redraw_board(state)
    app.update()


root = tkinter.Tk()
root.geometry('620x620')
root.resizable(0, 0)
app = Board(root)
