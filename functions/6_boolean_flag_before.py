from dataclasses import dataclass
from enum import StrEnum, auto

FIXED_VACATION_DAYS_PAYOUT = 5


class Role(StrEnum):
    PRESIDENT = auto()
    VICEPRESIDENT = auto()
    MANAGER = auto()
    LEAD = auto()
    ENGINEER = auto()
    INTERN = auto()


@dataclass
class Employee:
    name: str
    role: Role
    vacation_days: int = 25

    def take_a_holiday(self, payout: bool, nr_days: int = 1) -> None:
        if payout:
            if self.vacation_days < FIXED_VACATION_DAYS_PAYOUT:
                raise ValueError(
                    f"You don't have enough holidays left over for a payout.\
                        Remaining holidays: {self.vacation_days}."
                )
            self.vacation_days -= FIXED_VACATION_DAYS_PAYOUT
            print(f"Paying out a holiday. Holidays left: {self.vacation_days}")
        else:
            if self.vacation_days < nr_days:
                raise ValueError(
                    "You don't have any holidays left. Now back to work, you!"
                )
            self.vacation_days -= nr_days
            print("Have fun on your holiday. Don't forget to check your emails!")


def main() -> None:
    employee = Employee(name="John Doe", role=Role.ENGINEER)
    employee.take_a_holiday(True)


if __name__ == "__main__":
    main()
