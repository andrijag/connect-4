import tkinter as tk

from .model import Game
from .view import View


class Application(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Connect 4")

        model = Game()
        view = View(self, model)

        model.attach_observer(view)
        model.notify_observers()

        view.pack(expand=True, fill="both")
