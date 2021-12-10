import pytest


def add_three(x: int) -> int:
    return x + 3


def remove_three(x: int) -> int:
    return x - 3


@pytest.mark.parametrize("value", range(10))
def test_add_remove(value: int):
    assert remove_three(add_three(value)) == value
