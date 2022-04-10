from dataclasses import dataclass


@dataclass
class Employee:
    name: str
    role: str


def main() -> None:
    louis = Employee(name="Louis", role="staff")
    print(louis)
    sarah = Employee(name="Sarah", role="ceo")
    print(sarah)


if __name__ == "__main__":
    main()
