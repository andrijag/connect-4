import tkinter as tk
from .model import Game
from .view import View

N_ROWS = 6
N_COLUMNS = 7
CONNECT_N = 4


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Connect-4")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        model = Game(N_ROWS, N_COLUMNS, CONNECT_N)
        view = View(self, N_ROWS, N_COLUMNS)

        model.attach_observer(view)
        model.notify_observers()

        view.grid(column=0, row=0, sticky="nsew")
