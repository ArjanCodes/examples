from dataclasses import dataclass


@dataclass
class Employee:
    """Basic representation of an employee at the company."""

    name: str
    role: str
    vacation_days: int = 25

    def payout_holiday(self) -> None:
        """Let the employee take a single holiday, or pay out 5 holidays."""
        self._withdraw_holiday(5)
        print(f"Paying out a holiday. Holidays left: {self.vacation_days}")

    def take_single_holiday(self) -> None:
        """Let the employee take a single holiday."""
        # check whether self.vacation_days is less than 1
        self._withdraw_holiday(1)
        print("Have fun on your holiday. Don't forget to check your emails!")

    def _withdraw_holiday(self, days: int) -> None:
        """Withdraw a number of holidays."""
        if self.vacation_days < days:
            raise ValueError(
                f"You don't have enough holidays left over for a withdrawal.\
                    Remaining holidays: {self.vacation_days}."
            )
        self.vacation_days -= days
