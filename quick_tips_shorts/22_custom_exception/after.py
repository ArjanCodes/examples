from dataclasses import dataclass


@dataclass
class VacationDaysShortageError(Exception):
    requested_days: int
    remaining_days: int


@dataclass
class Employee:

    name: str
    vacation_days: int = 25

    def take_holiday(self, days: int = 1) -> None:
        if self.vacation_days < days:
            raise VacationDaysShortageError(
                requested_days=days,
                remaining_days=self.vacation_days,
            )
        self.vacation_days -= days
        print("Have fun on your holiday. Don't forget to check your emails!")


def main() -> None:
    try:
        louis = Employee(name="Louis")
        louis.take_holiday(30)
    except VacationDaysShortageError as err:
        print(
            f"{err.requested_days} days requested, but only {err.remaining_days} left"
        )


if __name__ == "__main__":
    main()
