from dataclasses import dataclass
from enum import Enum


class OrganizationRole(Enum):
    CEO = "ceo"
    PRESIDENT = "president"
    MANAGER = "manager"
    STAFF = "staff"


@dataclass
class Employee:
    name: str
    role: OrganizationRole


def main() -> None:
    louis = Employee(name="Louis", role=OrganizationRole.STAFF)
    print(louis)
    sarah = Employee(name="Sarah", role=OrganizationRole.CEO)
    print(sarah)


if __name__ == "__main__":
    main()
