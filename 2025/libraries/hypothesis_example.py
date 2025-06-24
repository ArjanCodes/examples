from hypothesis import given
from hypothesis.strategies import integers, lists


@given(lists(integers()))
def test_sort_idempotent(xs: list[int]) -> None:
    assert sorted(sorted(xs)) == sorted(xs)
