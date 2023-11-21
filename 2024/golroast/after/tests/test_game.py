from game import Game
from rules import birth_rule, lonely_death_rule, stay_alive_rule, over_populate_rule

RULES = [birth_rule, lonely_death_rule, stay_alive_rule, over_populate_rule]


def test_grid_1() -> None:
    initial_state = [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
    expected_state = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]

    game = Game(3, 3, RULES)
    game.grid.grid = initial_state
    game.update()
    assert game.grid.grid == expected_state


def test_grid_2() -> None:
    initial_state = [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]]
    expected_state = [[1, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 1]]

    game = Game(4, 4, RULES)
    game.grid.grid = initial_state
    game.update()
    assert game.grid.grid == expected_state


def test_grid_3() -> None:
    initial_state = [[1, 1, 1], [1, 1, 1], [0, 1, 0]]
    expected_state = [[1, 0, 1], [0, 0, 0], [1, 1, 1]]

    game = Game(3, 3, RULES)
    game.grid.grid = initial_state
    game.update()
    assert game.grid.grid == expected_state
