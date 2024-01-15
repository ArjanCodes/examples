from rules import birth_rule


def test_birth_rule_with_dead_cell_and_three_live_neighbors():
    assert birth_rule(0, 3) == 1


def test_birth_rule_with_dead_cell_and_two_live_neighbors():
    assert birth_rule(0, 2) is None


def test_birth_rule_with_alive_cell():
    assert birth_rule(1, 3) is None


def test_birth_rule_with_dead_cell_and_four_live_neighbors():
    assert birth_rule(0, 4) is None
