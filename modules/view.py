from collections.abc import Callable
import tkinter as tk
from tkinter import ttk

from .model import Observer, Game


class View(ttk.Frame, Observer):
    def __init__(self, parent: tk.Misc, model: Game) -> None:
        super().__init__(parent)
        self._model = model
        token_colors = ["red", "yellow"]
        self._player_color = {
            player.id_: token_colors[i] for i, player in enumerate(model.players)
        }

        self._score = ttk.Label(self, text="score")
        self._grid_view = GridView(self, model.n_rows, model.n_columns)
        for i in range(model.n_rows):
            for j in range(model.n_columns):
                self._grid_view.get(i, j).bind(
                    "<Button-1>", lambda event, column=j: self._click(column)
                )
        ttk.Button(self, text="Restart", command=self._restart)

        for child in self.winfo_children():
            child.pack(expand=True, padx=10, pady=10)

    def _click(self, column: int) -> None:
        self._model.drop(column)

    def _restart(self) -> None:
        self._model.restart()

    def update_(self) -> None:
        self._update_score()
        self._update_grid()

    def _update_score(self) -> None:
        score = self._get_score()
        self._score["text"] = score

    def _get_score(self) -> str:
        return " / ".join(str(player.score) for player in self._model.players)

    def _update_grid(self) -> None:
        for row in range(self._model.n_rows):
            for column in range(self._model.n_columns):
                grid_cell = self._grid_view.get(row, column)
                value = self._model.grid[row][column]
                if value:
                    token = self._player_color[value]
                    grid_cell.fill(token)
                else:
                    grid_cell.clear()


class GridView(tk.Canvas):
    def __init__(
        self, parent: tk.Misc, n_rows: int = 6, n_columns: int = 7, cell_size: int = 50
    ) -> None:
        canvas_width = n_columns * cell_size
        canvas_height = n_rows * cell_size
        super().__init__(
            parent, width=canvas_width, height=canvas_height, highlightthickness=0
        )

        self._create_frame(canvas_width, canvas_height)
        self._grid = self._create_grid(n_rows, n_columns, cell_size)

    def _create_frame(self, width: int, height: int) -> None:
        self.create_rectangle(
            0, 0, width, height, width=10, outline="dark blue", fill="medium blue"
        )

    def _create_grid(
        self, n_rows: int, n_columns: int, cell_size: int
    ) -> list[list["GridCell"]]:
        grid = []
        for i in range(n_rows):
            row = []
            for j in range(n_columns):
                x0 = j * cell_size
                y0 = i * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                row.append(GridCell(self, x0, y0, x1, y1))
            grid.append(row)
        return grid

    def get(self, row: int, column: int) -> "GridCell":
        return self._grid[row][column]


class GridCell:
    def __init__(self, canvas: tk.Canvas, x0: int, y0: int, x1: int, y1: int) -> None:
        self._canvas = canvas
        ipad = 5
        self._id = canvas.create_oval(
            x0 + ipad,
            y0 + ipad,
            x1 - ipad,
            y1 - ipad,
            width=5,
            fill="blue",
            outline="dark blue",
        )

    def bind(self, event: str, command: Callable[[tk.Event], None]) -> None:
        self._canvas.tag_bind(self._id, event, command)

    def fill(self, color: str) -> None:
        self._canvas.itemconfig(self._id, fill=color)

    def clear(self) -> None:
        self.fill("blue")
