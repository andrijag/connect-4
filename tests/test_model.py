import pytest

from modules.model import Grid, Player


class TestGrid:
    def test_stack_empty_column(self):
        n_rows = 6
        n_columns = 7
        grid = Grid(n_rows, n_columns)

        column = 0
        value = 1
        grid.stack(column, value)

        bottom_row = -1
        assert grid[bottom_row][column] == value

    def test_stack_consecutive(self):
        n_rows = 6
        n_columns = 7
        grid = Grid(n_rows, n_columns)

        column = 0
        value = 1

        for _ in range(n_rows):
            grid.stack(column, value)

        row = -n_rows
        assert grid[row][column] == value

    def test_stack_filled_column(self):
        n_rows = 6
        n_columns = 7
        grid = Grid(n_rows, n_columns)

        column = 0
        value = 1

        for _ in range(n_rows):
            grid.stack(column, value)

        with pytest.raises(IndexError):
            grid.stack(column, value)

    def test_is_filled(self):
        n_rows = 6
        n_columns = 7
        grid = Grid(n_rows, n_columns)

        value = 1

        for column in range(n_columns):
            for _ in range(n_rows):
                grid.stack(column, value)

        assert grid.is_filled()

    def test_is_not_filled(self):
        n_rows = 6
        n_columns = 7
        grid = Grid(n_rows, n_columns)

        assert not grid.is_filled()

    def test_is_filled_partially(self):
        n_rows = 6
        n_columns = 7
        grid = Grid(n_rows, n_columns)

        column = 0
        value = 1

        for _ in range(n_rows):
            grid.stack(column, value)

        assert not grid.is_filled()


class TestPlayer:
    def test_drop(self):
        id_ = 1
        player = Player(id_)

        n_rows = 6
        n_columns = 7
        grid = Grid(n_rows, n_columns)

        column = 0
        player.drop(grid, column)

        bottom_row = -1
        assert grid[bottom_row][column] == player.id_


class TestEvaluator:
    pass


class TestGame:
    pass
