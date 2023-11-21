from ..game_of_life import OverPopulateRule


def test_over_populate_rule_with_alive_cell_and_four_live_neighbors():
    assert OverPopulateRule.apply(1, 4) == 0


def test_over_populate_rule_with_alive_cell_and_five_live_neighbors():
    assert OverPopulateRule.apply(1, 5) == 0


def test_over_populate_rule_with_alive_cell_and_three_live_neighbors():
    assert OverPopulateRule.apply(1, 3) is None


def test_over_populate_rule_with_dead_cell():
    assert OverPopulateRule.apply(0, 4) is None
