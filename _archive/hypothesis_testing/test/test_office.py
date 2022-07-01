from typing import Callable

from hypothesis import given
from hypothesis.strategies import SearchStrategy, composite, integers
from hypothesis_testing.office import (
    Employee,
    fire_random_employee,
    generate_random_team,
)


@composite
def teams(
    draw: Callable[[SearchStrategy[int]], int], min_size: int = 1, max_size: int = 10
) -> list[Employee]:
    rand_val = draw(integers(min_value=min_size, max_value=max_size))
    return generate_random_team(rand_val)


@given(integers(min_value=1, max_value=10))
def test_team_size(team_size: int):
    assert len(generate_random_team(team_size)) == team_size


@given(teams(min_size=1))
def test_team_has_ceo(team: list[Employee]):
    assert Employee.CEO in team


@given(teams(min_size=1))
def test_fire_employee(team: list[Employee]):
    emp_list_copy = team.copy()
    fire_random_employee(emp_list_copy)
    assert len(emp_list_copy) == len(team) - 1
