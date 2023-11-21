import pytest
from ..game_of_life import Grid


@pytest.fixture
def grid():
    return Grid(3, 3)  # Create a 3x3 grid for testing


def test_initialization(grid: Grid) -> None:
    assert len(grid.grid) == 3
    assert len(grid.grid[0]) == 3


def test_is_cell_in_bounds(grid: Grid) -> None:
    assert grid.is_cell_in_bounds(0, 0) is True
    assert grid.is_cell_in_bounds(2, 2) is True
    assert grid.is_cell_in_bounds(-1, 0) is False
    assert grid.is_cell_in_bounds(0, 3) is False
    assert grid.is_cell_in_bounds(3, 0) is False
    assert grid.is_cell_in_bounds(3, 3) is False


def test_is_alive_with_dead_cell(grid: Grid) -> None:
    assert grid.is_alive(1, 1) == 0


def test_is_alive_with_alive_cell(grid: Grid) -> None:
    grid.grid[1][1] = 1
    assert grid.is_alive(1, 1) == 1


def test_is_alive_with_out_of_bounds_cell(grid: Grid) -> None:
    assert grid.is_alive(-1, 1) == 0


def test_alive_neighbors_for_center_cell(grid: Grid) -> None:
    grid.grid[0][1] = 1
    grid.grid[1][0] = 1
    grid.grid[1][2] = 1
    assert grid.alive_neighbors(1, 1) == 3


def test_alive_neighbors_for_corner_cell(grid: Grid) -> None:
    grid.grid[0][1] = 1
    grid.grid[1][0] = 1
    assert grid.alive_neighbors(0, 0) == 2
