from itertools import cycle


class Subject:
    def __init__(self):
        self._observers = []

    def attach_observer(self, observer):
        self._observers.append(observer)

    def detach_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update_()


class Game(Subject):
    def __init__(self, n_rows, n_columns, connect_n, n_players=2):
        super().__init__()
        self.players = [Player(i) for i in range(1, n_players + 1)]
        self._iterator = cycle(self.players)
        self._player = next(self._iterator)
        self.grid = Grid(n_rows, n_columns)
        self._validator = Validator(self.grid, connect_n)
        self._game_over = False

    def drop(self, i):
        if self._legal_move(i):
            self._player.drop(self.grid, i)
            if self._winning_move(i):
                self._end_game()
            else:
                self._next_turn()
            self.notify_observers()

    def _legal_move(self, i):
        return not self._game_over and not self.grid[i][-1]

    def _winning_move(self, i):
        for j in reversed(range(self.grid.n_rows)):
            if self.grid[i][j]:
                return self._validator.check(i, j)

    def _end_game(self):
        self._game_over = True
        self._player.score += 1

    def _next_turn(self):
        self._player = next(self._iterator)

    def restart(self):
        self._iterator = cycle(self.players)
        self._player = next(self._iterator)
        self.grid.reset()
        self._game_over = False
        self.notify_observers()


class Player:
    def __init__(self, id_):
        self.id_ = id_
        self.score = 0

    def __str__(self):
        return f"player {self.id_}"

    def drop(self, grid, i):
        grid.stack(i, self.id_)


class Grid:
    def __init__(self, n_rows, n_columns):
        self._grid = [[0 for _ in range(n_rows)] for _ in range(n_columns)]
        self.n_rows = n_rows
        self.n_columns = n_columns

    def __getitem__(self, key):
        return self._grid[key]

    def __str__(self):
        return str(self._grid)

    def reset(self):
        for i in range(self.n_columns):
            for j in range(self.n_rows):
                self._grid[i][j] = 0

    def stack(self, i, value):
        for j in range(self.n_rows):
            if not self._grid[i][j]:
                self._grid[i][j] = value
                break


class Validator:
    def __init__(self, matrix, connect_n):
        self._matrix = matrix
        self._connect_n = connect_n
        self._vectors = {
            "horizontal": (0, 1),
            "vertical": (1, 0),
            "diagonal": (1, 1),
            "anti-diagonal": (-1, 1),
        }

    def check(self, i, j):
        for di, dj in self._vectors.values():
            if self._count_in_direction(i, j, di, dj) >= self._connect_n:
                return True

    def _count_in_direction(self, i, j, di, dj):
        direction = self._count_consecutive(i, j, di, dj)
        opposite_direction = self._count_consecutive(i, j, -di, -dj)
        return direction + opposite_direction - 1

    def _count_consecutive(self, i, j, di, dj):
        if (
            i + di in range(self._matrix.n_columns)
            and j + dj in range(self._matrix.n_rows)
            and self._matrix[i][j] == self._matrix[i + di][j + dj]
        ):
            return 1 + self._count_consecutive(i + di, j + dj, di, dj)
        return 1
