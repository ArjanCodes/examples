from enum import Enum, auto


class OrganizationRoleWithAuto(Enum):
    CEO = auto()
    PRESIDENT = auto()
    MANAGER = auto()
    STAFF = auto()


class OrganizationRoleWithRange(Enum):
    CEO, PRESIDENT, MANAGER, STAFF = range(4)


class OrganizationRole(Enum):
    CEO = "ceo"
    PRESIDENT = "president"
    MANAGER = "manager"
    STAFF = "staff"


def main():
    my_role = OrganizationRole.PRESIDENT
    print(my_role)
    print(my_role.value)


if __name__ == "__main__":
    main()
