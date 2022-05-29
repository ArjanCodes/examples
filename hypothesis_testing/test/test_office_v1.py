from typing import Callable

from hypothesis import given, settings
from hypothesis.strategies import integers

from ..office import Employee, fire_random_employee, generate_random_team


@given(integers())
def test_team_size(team_size: int):
    assert len(generate_random_team(team_size)) == team_size


@given(integers())
def test_team_has_ceo(team_size: int):
    team = generate_random_team(team_size)
    assert Employee.CEO in team


@given(integers())
def test_fire_employee(team_size: int):
    team = generate_random_team(team_size)
    emp_list_copy = team.copy()
    fire_random_employee(emp_list_copy)
    assert len(emp_list_copy) == len(team) - 1
