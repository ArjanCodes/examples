from typing import Callable

from hypothesis import given
from hypothesis.strategies import SearchStrategy, composite, integers
from hypothesis_testing.office import (
    Employee,
    fire_random_employee,
    generate_random_team,
)


@composite
def employee_list(
    draw: Callable[[SearchStrategy[int]], int], min_size: int = 1, max_size: int = 10
) -> list[Employee]:
    rand_val = draw(integers(min_value=min_size, max_value=max_size))
    print(rand_val)
    return generate_random_team(rand_val)


@given(integers(min_value=1, max_value=10))
def test_team_size(team_size: int):
    assert len(generate_random_team(team_size)) == team_size


@given(employee_list(min_size=1))
def test_fire_employee(empl_list: list[Employee]):
    emp_list_copy = empl_list.copy()
    fire_random_employee(emp_list_copy)
    assert len(emp_list_copy) == len(empl_list) - 1
