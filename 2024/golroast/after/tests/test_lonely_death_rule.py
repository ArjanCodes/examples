from rules import lonely_death_rule


def test_lonely_death_rule_with_alive_cell_and_one_live_neighbor():
    assert lonely_death_rule(1, 1) == 0


def test_lonely_death_rule_with_alive_cell_and_zero_live_neighbors():
    assert lonely_death_rule(1, 0) == 0


def test_lonely_death_rule_with_alive_cell_and_two_live_neighbors():
    assert lonely_death_rule(1, 2) is None


def test_lonely_death_rule_with_dead_cell():
    assert lonely_death_rule(0, 1) is None
