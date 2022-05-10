import random
from enum import Enum, auto


class Employee(Enum):
    """Employee type"""

    CEO = auto()
    MANAGER = auto()
    SALES = auto()
    ENGINEER = auto()
    MARKETING = auto()
    ACCOUNTING = auto()
    IT = auto()
    HR = auto()
    OTHER = auto()


def generate_random_team(size: int) -> list[Employee]:
    """Generate a random team with exactly one CEO."""
    if size <= 0:
        raise ValueError("Team size must be greater than 0.")

    # team members without CEO
    team_no_ceo = list(Employee)
    team_no_ceo.remove(Employee.CEO)

    # generate a random team with one CEO
    team = [Employee.CEO]
    for _ in range(size - 1):
        team.append(random.choice(team_no_ceo))
    return team


def fire_random_employee(team: list[Employee]) -> None:
    """Fire a random employee from the team and the CEO last."""

    # create a copy of the team without the CEO
    team_no_ceo = team.copy()
    team_no_ceo.remove(Employee.CEO)

    if len(team_no_ceo) > 0:
        # remove a random employee from the team
        team.remove(random.choice(team_no_ceo))
    else:
        # remove the CEO from the team
        team.remove(Employee.CEO)
