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

        self._fixedAspectRatio = FixedAspectRatioDecorator(self, width=400, height=300, bg="red")
        self._canvas = Canvas(self._fixedAspectRatio, width=400, height=300, bg="blue")

        self._score = ScoreBoard(self)
        self._grid_view = GridView(self, model.n_rows, model.n_columns)
        for i in range(model.n_columns):
            for j in range(model.n_rows):
                self._grid_view.get(i, j).bind(
                    "<Button-1>", lambda event, x=i: self._click(x)
                )
        restart_button = tk.Button(self, text="Restart", command=self._restart)

        self._fixedAspectRatio.grid(column=0, row=1, padx=10, pady=10, sticky="nsew")

        self._score.grid(column=0, row=0, padx=10, pady=10)
        # self._grid_view.grid(column=0, row=1, padx=10, pady=10, sticky="nsew")
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


class Decorator(ABC):
    @abstractmethod
    def resize(self, event):
        pass


class FixedAspectRatioDecorator(tk.Frame, Decorator):
    def __init__(self, parent, *, width, height, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)

        self.bind("<Configure>", self.resize)

        self.aspect_ratio = width / height
        self._widget = None
        self._widget = Canvas(self, width=width, height=height, bg="blue")

        self._widget.place(
            width=width, height=height, anchor="center", x=width / 2, y=height / 2
        )

    def resize(self, event):
        widget_width = min(event.height * self.aspect_ratio, event.width)
        widget_height = min(event.height, event.width / self.aspect_ratio)
        self._widget.place(
            width=widget_width,
            height=widget_height,
            anchor="center",
            x=event.width / 2,
            y=event.height / 2,
        )
        self.configure(width=event.width, height=event.height)


class Canvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs, highlightthickness=0)

        self.bind("<Configure>", self.resize)

        self.create_line(
            0, kwargs["height"], kwargs["width"], 0, fill="yellow", width=10
        )

    def resize(self, event):
        width_ratio = event.width / float(self["width"])
        height_ratio = event.height / float(self["height"])
        self.scale("all", 0, 0, width_ratio, height_ratio)
        self.configure(width=event.width, height=event.height)


class GridView(tk.Canvas):
    def __init__(self, master, n_rows, n_columns, square_width=80):
        canvas_width = square_width * n_columns
        canvas_height = square_width * n_rows
        super().__init__(
            master, width=canvas_width, height=canvas_height, highlightthickness=0
        )

        self.bind("<Configure>", self._resize)

        self._create_frame(canvas_width, canvas_height)
        self._board = self._create_grid(n_rows, n_columns, square_width)

    def _resize(self, event):
        width_ratio = event.width / self.winfo_reqwidth()
        height_ratio = event.height / self.winfo_reqheight()
        self.scale("all", 0, 0, width_ratio, height_ratio)
        self.configure(width=event.width, height=event.height)

    def _create_frame(self, width, height):
        self.create_rectangle(
            0, 0, width, height, width=10, outline="dark blue", fill="medium blue"
        )

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

    def get(self, i, j):
        return self._board[i][j]


class GridCircle:
    def __init__(self, canvas, x0, y0, x1, y1, ipad=10):
        self._canvas = canvas
        x0 = x0 + ipad
        y0 = y0 + ipad
        x1 = x1 - ipad
        y1 = y1 - ipad
        self._id = canvas.create_oval(
            x0, y0, x1, y1, width=5, fill="blue", outline="dark blue"
        )

    def bind(self, event, command):
        self._canvas.tag_bind(self._id, event, command)

    def update(self, color):
        self._fill(color)

    def reset(self):
        self._fill("blue")

    def _fill(self, color):
        self._canvas.itemconfigure(self._id, fill=color)
