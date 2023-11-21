from game import Game
from grid import Grid
from rules import birth_rule, lonely_death_rule, stay_alive_rule, over_populate_rule

RULES = [birth_rule, lonely_death_rule, stay_alive_rule, over_populate_rule]


def test_grid_1() -> None:
    initial_state = [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
    expected_state = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]

    grid = Grid(3, 3, initial_state)
    game = Game(grid, RULES)
    game.update()
    assert game.grid.grid == expected_state


def test_grid_2() -> None:
    initial_state = [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]]
    expected_state = [[1, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 1]]

    grid = Grid(4, 4, initial_state)
    game = Game(grid, RULES)
    game.update()
    assert game.grid.grid == expected_state


def test_grid_3() -> None:
    initial_state = [[1, 1, 1], [1, 1, 1], [0, 1, 0]]
    expected_state = [[1, 0, 1], [0, 0, 0], [1, 1, 1]]

    grid = Grid(3, 3, initial_state)
    game = Game(grid, RULES)
    game.update()
    assert game.grid.grid == expected_state
