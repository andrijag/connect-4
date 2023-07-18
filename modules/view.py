import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update_(self):
        pass


class View(ttk.Frame, Observer):
    def __init__(self, parent, model):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self._model = model
        self._colors = ["red", "yellow"]

        self._player_color = {
            player.id_: self._colors[i] for i, player in enumerate(model.players)
        }

        self._score = ScoreBoard(self)
        self._grid_view = GridView(self, model.n_rows, model.n_columns)
        for i in range(model.n_columns):
            for j in range(model.n_rows):
                self._grid_view.get(i, j).bind(
                    "<Button-1>", lambda event, x=i: self._click(x)
                )
        restart_button = tk.Button(self, text="Restart", command=self._restart)

        self._score.grid(column=0, row=0, padx=10, pady=10)
        self._grid_view.grid(column=0, row=1, padx=10, pady=10)
        restart_button.grid(column=0, row=2, padx=10, pady=10)

    def _click(self, i):
        self._model.drop(i)

    def _restart(self):
        self._model.restart()

    def update_(self):
        self._update_score()
        self._update_grid()

    def _update_score(self):
        score = self._get_score()
        self._score.update_(score)

    def _get_score(self):
        return " / ".join(str(player.score) for player in self._model.players)

    def _update_grid(self):
        for i in range(self._model.n_columns):
            for j in range(self._model.n_rows):
                grid_circle = self._grid_view.get(i, j)
                value = self._model.grid[i][j]
                if value:
                    token = self._player_color[value]
                    grid_circle.update(token)
                else:
                    grid_circle.reset()


class ScoreBoard(ttk.Label):
    def __init__(self, master):
        super().__init__(master, text="score")

    def update_(self, score):
        self.configure(text=score)


class GridView(tk.Canvas):
    def __init__(self, master, n_rows, n_columns):
        cell_size = 50
        canvas_width = n_columns * cell_size
        canvas_height = n_rows * cell_size
        super().__init__(
            master, width=canvas_width, height=canvas_height, highlightthickness=0
        )

        self._create_frame(canvas_width, canvas_height)
        self._board = self._create_grid(n_rows, n_columns, cell_size)

    def _create_frame(self, width, height):
        self.create_rectangle(
            0, 0, width, height, width=10, outline="dark blue", fill="medium blue"
        )

    def _create_grid(self, n_rows, n_columns, cell_size):
        grid = []
        for i in range(n_columns):
            column = []
            for j in reversed(range(n_rows)):
                x0 = i * cell_size
                y0 = j * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                column.append(GridCircle(self, x0, y0, x1, y1))
            grid.append(column)
        return grid

    def get(self, i, j):
        return self._board[i][j]


class GridCircle:
    def __init__(self, canvas, x0, y0, x1, y1):
        self._canvas = canvas
        ipad = 5
        self._id = canvas.create_oval(
            x0 + ipad, y0 + ipad, x1 - ipad, y1 - ipad, width=5, fill="blue", outline="dark blue"
        )

    def bind(self, event, command):
        self._canvas.tag_bind(self._id, event, command)

    def update(self, color):
        self._fill(color)

    def reset(self):
        self._fill("blue")

    def _fill(self, color):
        self._canvas.itemconfigure(self._id, fill=color)
