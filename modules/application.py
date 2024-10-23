import tkinter as tk

from .model import Game
from .view import View

N_ROWS = 6
N_COLUMNS = 7
CONNECT_N = 4


class Application(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Connect 4")

        model = Game(N_ROWS, N_COLUMNS, CONNECT_N)
        view = View(self, model)

        model.attach_observer(view)
        model.notify_observers()

        view.pack(expand=True, fill="both")
