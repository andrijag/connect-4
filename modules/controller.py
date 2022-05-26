from abc import ABC, abstractmethod


class ControllerStrategy(ABC):
    @abstractmethod
    def click(self, i, j):
        pass

    @abstractmethod
    def restart(self):
        pass

    @abstractmethod
    def update(self):
        pass


class Controller(ControllerStrategy):
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.player_color = {
            player.id_: view.colors[i] for i, player in enumerate(model.players)
        }

    def click(self, i, j):
        self.model.drop(i)

    def restart(self):
        self.model.restart()

    def update(self):
        self._update_score()
        self._update_board()

    def _update_score(self):
        score = self._get_score()
        self.view.score.update_(score)

    def _get_score(self):
        return " / ".join(str(player.score) for player in self.model.players)

    def _update_board(self):
        for i in range(self.model.grid.n_columns):
            for j in range(self.model.grid.n_rows):
                grid_circle = self.view.grid_view.get(i, j)
                value = self.model.grid[i][j]
                token = self.player_color.get(value, None)
                grid_circle.update(token)
