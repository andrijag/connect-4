from abc import ABC, abstractmethod


class ControllerStrategy(ABC):
    @abstractmethod
    def click(self, i):
        pass

    @abstractmethod
    def restart(self):
        pass

    @abstractmethod
    def update(self):
        pass


class Controller(ControllerStrategy):
    def __init__(self, model, view, bots=None):
        self.model = model
        self.view = view

        self.player_color = {
            player.id_: view.colors[i] for i, player in enumerate(model.players)
        }

    def click(self, i):
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
        return " : ".join(str(player.score) for player in self.model.players)

    def _update_board(self):
        for i in range(self.model.board.n_rows):
            for j in range(self.model.board.n_columns):
                grid_circle = self.view.board.get(i, j)
                value = self.model.board[i][j]
                token = self.player_color.get(value, None)
                grid_circle.update(token)
