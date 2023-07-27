import random
import functools


def roll_n_dice(n_dice: int, n_sides: int) -> int:
    """Rolls n_dice dice, each die has n_sides, and returns the total"""
    rolls = [random.randint(1, n_sides) for _ in range(n_dice)]
    return sum(rolls)


roll_n_d6 = functools.partial(roll_n_dice, n_sides=6)
roll_n_d20 = functools.partial(roll_n_dice, n_sides=20)