from enum import Enum


class OrganizationRole(Enum):
    CEO = 0
    PRESIDENT = 1
    MANAGER = 2
    STAFF = 3


def main():
    my_role = OrganizationRole.MANAGER
    print(my_role)
    print(my_role.value)


if __name__ == "__main__":
    main()
