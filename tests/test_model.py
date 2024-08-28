import pytest

from modules.model import Grid, Player


class TestGrid:
    @pytest.fixture
    def grid(self):
        n_rows = 6
        n_columns = 7
        return Grid(n_rows, n_columns)

    def test_stack_empty_column(self, grid):
        column = 0
        value = 1
        grid.stack(column, value)

        bottom_row = -1
        assert grid[bottom_row][column] == value

    def test_stack_consecutive(self, grid):
        column = 0
        value = 1

        for _ in range(grid.n_rows):
            grid.stack(column, value)

        row = -grid.n_rows
        assert grid[row][column] == value

    def test_stack_filled_column(self, grid):
        with pytest.raises(IndexError):
            column = 0
            value = 1

            for _ in range(grid.n_rows):
                grid.stack(column, value)

            grid.stack(column, value)
