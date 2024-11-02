import pytest

from modules.model import Grid, Player, Evaluator


class TestGrid:
    @staticmethod
    def stack_consecutive(n: int, grid: Grid, column: int, value: int) -> int:
        if n < 1:
            raise ValueError("parameter n < 1")
        for _ in range(n - 1):
            grid.stack(column, value)
        return grid.stack(column, value)

    @pytest.mark.parametrize("n", [1, 2])
    def test_stack_return(self, n) -> None:
        grid = Grid()

        n = 2
        first_column = 0
        value = 1
        row = TestGrid.stack_consecutive(n, grid, first_column, value)

        stack_row = grid.n_rows - n
        assert row == stack_row

    @pytest.mark.parametrize("n", [1, 2])
    def test_stack(self, n) -> None:
        grid = Grid()

        first_column = 0
        value = 1
        row = TestGrid.stack_consecutive(n, grid, first_column, value)

        assert grid[row][first_column] == value

    def test_stack_empty_column(self) -> None:
        grid = Grid()

        first_column = 0
        value = 1
        row = grid.stack(first_column, value)

        assert grid[row][first_column] == value

    def test_stack_consecutive(self) -> None:
        grid = Grid()

        n = 2
        first_column = 0
        value = 1
        row = TestGrid.stack_consecutive(n, grid, first_column, value)

        assert grid[row][first_column] == value

    def test_stack_filled_column_error(self) -> None:
        grid = Grid()

        first_column = 0
        value = 1
        TestGrid.stack_consecutive(grid.n_rows, grid, first_column, value)

        with pytest.raises(IndexError):
            grid.stack(first_column, value)

    def test_is_filled(self) -> None:
        grid = Grid()

        value = 1
        for column in range(grid.n_columns):
            TestGrid.stack_consecutive(grid.n_rows, grid, column, value)

        assert grid.is_filled()

    def test_is_not_filled_empty_grid(self) -> None:
        grid = Grid()

        assert not grid.is_filled()

    def test_is_not_filled_partially_filled(self) -> None:
        grid = Grid()

        first_column = 0
        value = 1
        TestGrid.stack_consecutive(grid.n_rows, grid, first_column, value)

        assert not grid.is_filled()


class TestPlayer:
    def test_drop(self) -> None:
        id_ = 1
        player = Player(id_)
        grid = Grid()

        first_column = 0
        row = player.drop(grid, first_column)

        assert grid[row][first_column] == player.id_


class TestEvaluator:
    def test_check_false(self) -> None:
        grid = Grid()
        evaluator = Evaluator(grid)

        first_column = 0
        bottom_row = grid.n_rows - 1
        assert not evaluator.check(bottom_row, first_column)

    def test_check_true(self) -> None:
        grid = Grid()
        evaluator = Evaluator(grid)

        first_column = 0
        value = 1
        row = TestGrid.stack_consecutive(evaluator.connect_n, grid, first_column, value)

        assert evaluator.check(row, first_column)


class TestGame:
    pass
