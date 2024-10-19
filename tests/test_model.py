import pytest

from modules.model import Grid, Player


class TestGrid:
    def test_stack_empty_column(self):
        grid = Grid()

        first_column = 0
        value = 1
        grid.stack(first_column, value)

        bottom_row = -1
        assert grid[bottom_row][first_column] == value

    def test_stack_consecutive(self):
        grid = Grid()

        first_column = 0
        value = 1
        for _ in range(grid.n_rows):
            grid.stack(first_column, value)

        row = -grid.n_rows
        assert grid[row][first_column] == value

    def test_stack_filled_column(self):
        grid = Grid()

        first_column = 0
        value = 1
        for _ in range(grid.n_rows):
            grid.stack(first_column, value)

        with pytest.raises(IndexError):
            grid.stack(first_column, value)

    def test_is_filled(self):
        grid = Grid()

        value = 1
        for column in range(grid.n_columns):
            for _ in range(grid.n_rows):
                grid.stack(column, value)

        assert grid.is_filled()

    def test_is_not_filled(self):
        grid = Grid()

        assert not grid.is_filled()

    def test_is_filled_partially(self):
        grid = Grid()

        first_column = 0
        value = 1
        for _ in range(grid.n_rows):
            grid.stack(first_column, value)

        assert not grid.is_filled()


class TestPlayer:
    def test_drop(self):
        id_ = 1
        player = Player(id_)
        grid = Grid()

        first_column = 0
        player.drop(grid, first_column)

        bottom_row = -1
        assert grid[bottom_row][first_column] == player.id_


class TestEvaluator:
    pass


class TestGame:
    pass
