from rules import StayAliveRule


def test_stay_alive_rule_with_alive_cell_and_two_live_neighbors():
    assert StayAliveRule.apply(1, 2) == 1


def test_stay_alive_rule_with_alive_cell_and_three_live_neighbors():
    assert StayAliveRule.apply(1, 3) == 1


def test_stay_alive_rule_with_alive_cell_and_one_live_neighbor():
    assert StayAliveRule.apply(1, 1) is None


def test_stay_alive_rule_with_alive_cell_and_four_live_neighbors():
    assert StayAliveRule.apply(1, 4) is None


def test_stay_alive_rule_with_dead_cell():
    assert StayAliveRule.apply(0, 2) is None
