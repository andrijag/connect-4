from abc import ABC, abstractmethod
from itertools import cycle


class Subject:
    def __init__(self) -> None:
        self._observers = []

    def attach_observer(self, observer: "Observer") -> None:
        self._observers.append(observer)

    def detach_observer(self, observer: "Observer") -> None:
        self._observers.remove(observer)

    def notify_observers(self) -> None:
        for observer in self._observers:
            observer.update_()


class Observer(ABC):
    @abstractmethod
    def update_(self) -> None:
        pass


class Game(Subject):
    def __init__(
        self,
        n_rows: int = 6,
        n_columns: int = 7,
        connect_n: int = 4,
        n_players: int = 2,
    ) -> None:
        super().__init__()
        self.players = [Player(id_) for id_ in range(1, n_players + 1)]
        self._iterator = cycle(self.players)
        self._player = next(self._iterator)
        self.grid = Grid(n_rows, n_columns)
        self._evaluator = Evaluator(self.grid, connect_n)
        self._game_over = False
        self.winner = None

    @property
    def n_rows(self) -> int:
        return self.grid.n_rows

    @property
    def n_columns(self) -> int:
        return self.grid.n_columns

    @property
    def connect_n(self) -> int:
        return self._evaluator.connect_n

    def drop(self, column: int) -> None:
        if not self._legal_move(column):
            return
        self._player.drop(self.grid, column)
        if self._winning_move(column):
            self._end_game()
            self._add_score()
        elif self.grid.is_filled():
            self._end_game()
        else:
            self._next_turn()
        self.notify_observers()

    def _legal_move(self, column: int) -> bool:
        top_row = 0
        return not self._game_over and not self.grid[top_row][column]

    def _winning_move(self, column: int) -> bool:
        for row in range(self.n_rows):
            if self.grid[row][column]:
                return self._evaluator.check(row, column)
        return False

    def _end_game(self) -> None:
        self._game_over = True

    def _add_score(self) -> None:
        self.winner = self._player
        self.winner.score += 1

    def _next_turn(self) -> None:
        self._player = next(self._iterator)

    def restart(self) -> None:
        self._iterator = cycle(self.players)
        self._player = next(self._iterator)
        self.grid = Grid(self.n_rows, self.n_columns)
        self._evaluator = Evaluator(self.grid, self.connect_n)
        self._game_over = False
        self.winner = None
        self.notify_observers()


class Player:
    def __init__(self, id_: int) -> None:
        self.id_ = id_
        self.score = 0

    def __str__(self) -> str:
        return f"player {self.id_}"

    def drop(self, grid: "Grid", column: int) -> None:
        grid.stack(column, self.id_)


class Grid:
    def __init__(self, n_rows: int = 6, n_columns: int = 7) -> None:
        self.n_rows = n_rows
        self.n_columns = n_columns
        self._matrix = [[0 for _ in range(n_columns)] for _ in range(n_rows)]

    def __getitem__(self, key: int) -> list[int] | int:
        return self._matrix[key]

    def __str__(self) -> str:
        return str(self._matrix)

    def stack(self, column: int, value: int) -> None:
        for row in reversed(range(self.n_rows)):
            if not self._matrix[row][column]:
                self._matrix[row][column] = value
                return
        raise IndexError

    def is_filled(self) -> bool:
        return all(all(row) for row in self._matrix)


class Evaluator:
    def __init__(self, grid: Grid, connect_n: int = 4) -> None:
        self._grid = grid
        self.connect_n = connect_n
        self._vectors = {
            "horizontal": (0, 1),
            "vertical": (1, 0),
            "diagonal": (1, 1),
            "anti-diagonal": (-1, 1),
        }

    def check(self, i: int, j: int) -> bool:
        if not self._grid[i][j]:
            return False
        for di, dj in self._vectors.values():
            if self._count_in_direction(i, j, di, dj) >= self.connect_n:
                return True
        return False

    def _count_in_direction(self, i: int, j: int, di: int, dj: int) -> int:
        direction = self._count_consecutive(i, j, di, dj)
        opposite_direction = self._count_consecutive(i, j, -di, -dj)
        return direction + opposite_direction - 1

    def _count_consecutive(self, i: int, j: int, di: int, dj: int) -> int:
        if (
            i + di in range(self._grid.n_rows)
            and j + dj in range(self._grid.n_columns)
            and self._grid[i][j] == self._grid[i + di][j + dj]
        ):
            return 1 + self._count_consecutive(i + di, j + dj, di, dj)
        return 1
