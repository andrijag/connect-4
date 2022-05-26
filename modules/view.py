import tkinter as tk
from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update_(self):
        pass


class View(tk.Frame, Observer):
    def __init__(self, parent, n_rows, n_columns):
        super().__init__(parent, background="blue")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.controller = None
        self.colors = ["red", "yellow"]

        self.score = ScoreBoard(self)
        self.grid_view = GridView(self, n_rows, n_columns)
        for i in range(n_columns):
            for j in range(n_rows):
                self.grid_view.get(i, j).bind(
                    "<Button-1>", lambda event, x=i, y=j: self._click(x, y)
                )
        self.restart_button = tk.Button(self, text="Restart", command=self._restart)

        self.score.configure(bg="blue", fg="white")
        self.grid_view.configure(bg="medium blue")
        self.restart_button.configure(bg="blue", fg="white", activebackground="blue", activeforeground="white", highlightthickness=0)

        self.score.grid(column=0, row=0, padx=10, pady=10)
        self.grid_view.grid(column=0, row=1, padx=10, pady=10)
        self.restart_button.grid(column=0, row=2, padx=10, pady=10)

    def _click(self, i, j):
        if self.controller:
            self.controller.click(i, j)

    def _restart(self):
        if self.controller:
            self.controller.restart()

    def update_(self):
        if self.controller:
            self.controller.update()


class ScoreBoard(tk.Label):
    def __init__(self, master):
        super().__init__(master, text="score")

    def update_(self, score):
        self.configure(text=score)


class GridView(tk.Canvas):
    def __init__(self, master, n_rows, n_columns, square_width=100):
        canvas_width = square_width * n_columns
        canvas_height = square_width * n_rows
        super().__init__(master, width=canvas_width, height=canvas_height, bg="blue", highlightthickness=0)

        self._board = self._create_grid(n_rows, n_columns, square_width)
        self._create_frame(canvas_width, canvas_height)

    def _create_grid(self, n_rows, n_columns, square_width):
        grid = []
        for i in range(n_columns):
            column = []
            for j in reversed(range(n_rows)):
                x0 = i * square_width
                y0 = j * square_width
                x1 = x0 + square_width
                y1 = y0 + square_width
                column.append(GridCircle(self, x0, y0, x1, y1))
            grid.append(column)
        return grid

    def _create_frame(self, width, height):
        self.create_rectangle(0, 0, width, height, width=10, outline="dark blue")

    def get(self, i, j):
        return self._board[i][j]


class GridCircle:
    def __init__(self, canvas, x0, y0, x1, y1, ipad=10):
        self.canvas = canvas
        x0 = x0 + ipad
        y0 = y0 + ipad
        x1 = x1 - ipad
        y1 = y1 - ipad
        self.id_ = canvas.create_oval(x0, y0, x1, y1, width=5, fill="blue", outline="dark blue")

    def bind(self, event, command):
        self.canvas.tag_bind(self.id_, event, command)

    def update(self, color):
        if color:
            self._fill(color)
        else:
            self._fill("blue")

    def _fill(self, color):
        self.canvas.itemconfigure(self.id_, fill=color)
