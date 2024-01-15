def birth_rule(cell: int, live_neighbors: int) -> int | None:
    if cell == 0 and live_neighbors == 3:
        return 1
    return None


def lonely_death_rule(cell: int, live_neighbors: int) -> int | None:
    if cell == 1 and live_neighbors < 2:
        return 0
    return None


def stay_alive_rule(cell: int, live_neighbors: int) -> int | None:
    if cell == 1 and 2 <= live_neighbors <= 3:
        return 1
    return None


def over_populate_rule(cell: int, live_neighbors: int) -> int | None:
    if cell == 1 and live_neighbors > 3:
        return 0
    return None
