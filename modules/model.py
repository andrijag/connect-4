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
            observer.update_observer()


class Game(Subject):
    def __init__(self, n_rows, n_columns, connect_n, n_players=2):
        super().__init__()
        self.n_rows = n_rows
        self.n_columns = n_columns
        self.connect_n = connect_n
        self.players = [Player(i) for i in range(1, n_players + 1)]
        self._iterator = cycle(self.players)
        self._player = next(self._iterator)
        self.grid = Grid(n_rows, n_columns)
        self._evaluator = Evaluator(self.grid, connect_n)
        self._game_over = False
        self.winner = None

    def drop(self, column):
        if self._game_over or not self._legal_move(column):
            return
        self._player.drop(self.grid, column)
        if self._winning_move(column):
            self._end_game()
            self._add_score()
        elif self._filled_grid():
            self._end_game()
        else:
            self._next_turn()
        self.notify_observers()

    def _legal_move(self, column):
        return not self.grid[0][column]

    def _winning_move(self, column):
        for row in range(self.grid.n_rows):
            if self.grid[row][column]:
                return self._evaluator.check(row, column)

    def _end_game(self):
        self._game_over = True

    def _add_score(self):
        self.winner = self._player
        self.winner.score += 1

    def _filled_grid(self):
        for row in range(self.n_rows):
            for column in range(self.n_columns):
                if not self.grid[row][column]:
                    return False
        return True

    def _next_turn(self):
        self._player = next(self._iterator)

    def restart(self):
        self._iterator = cycle(self.players)
        self._player = next(self._iterator)
        self.grid = Grid(self.n_rows, self.n_columns)
        self._evaluator = Evaluator(self.grid, self.connect_n)
        self._game_over = False
        self.winner = None
        self.notify_observers()


class Player:
    def __init__(self, id_):
        self.id_ = id_
        self.score = 0

    def __str__(self):
        return f"player {self.id_}"

    def drop(self, grid, column):
        grid.drop(column, self.id_)


class Grid:
    def __init__(self, n_rows, n_columns):
        self.n_rows = n_rows
        self.n_columns = n_columns
        self._matrix = [[0 for _ in range(n_columns)] for _ in range(n_rows)]

    def __getitem__(self, key):
        return self._matrix[key]

    def __str__(self):
        return str(self._matrix)

    def drop(self, column, value):
        for row in reversed(range(self.n_rows)):
            if not self._matrix[row][column]:
                self._matrix[row][column] = value
                return


class Evaluator:
    def __init__(self, grid, connect_n):
        self._grid = grid
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
            i + di in range(self._grid.n_rows)
            and j + dj in range(self._grid.n_columns)
            and self._grid[i][j] == self._grid[i + di][j + dj]
        ):
            return 1 + self._count_consecutive(i + di, j + dj, di, dj)
        return 1
