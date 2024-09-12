from dataclasses import dataclass


class Worker:
    def __init__(self) -> None:
        self.id = 0
        self.info = "Worker"


class Employee(Worker):
    def __init__(self, first_name: str, last_name: str, salary: int):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.salary = salary

    def give_raise(self, amount: int = 5000):
        self.salary += amount
        return self.salary


@dataclass
class Boss:
    first_name: str  # Not this
    last_name: str  # Not this

    def give_raise(self, amount: int) -> int:
        self.bonus += amount  # This will be logged as an static attribute
        return self.bonus


def main() -> None:
    print(Employee.__static_attributes__)

    e = Employee("John", "Doe", 50000)

    print(f"ID: {e.id}, Name: {e.first_name} {e.last_name}, Salary: {e.salary}")

    print(Boss.__static_attributes__)

    arjan = Boss("Arjan", "Codes")

    print(f"Name: {arjan.first_name} {arjan.last_name}")


if __name__ == "__main__":
    main()
