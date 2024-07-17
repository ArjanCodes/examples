class Employee:
    def get_details(self) -> str:
        return "Employee"


class Manager(Employee):
    def get_details(self) -> str:
        return "Manager"


class SeniorManager(Manager):
    def get_details(self) -> str:
        return "Senior Manager"


class Director(SeniorManager):
    def get_details(self) -> str:
        return "Director"


def main() -> None:
    manager = Manager()
    senior_manager = SeniorManager()
    director = Director()
    print(manager.get_details())
    print(senior_manager.get_details())
    print(director.get_details())


if __name__ == "__main__":
    main()
