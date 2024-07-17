from enum import StrEnum


class Role(StrEnum):
    EMPLOYEE = "Employee"
    MANAGER = "Manager"
    SENIOR_MANAGER = "Senior Manager"
    DIRECTOR = "Director"


class Employee:
    def __init__(self, role: Role) -> None:
        self.role = role

    def get_details(self):
        return self.role


def main() -> None:
    manager = Employee(Role.MANAGER)
    senior_manager = Employee(Role.SENIOR_MANAGER)
    director = Employee(Role.DIRECTOR)
    print(manager.get_details())
    print(senior_manager.get_details())
    print(director.get_details())


if __name__ == "__main__":
    main()
