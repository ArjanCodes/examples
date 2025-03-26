from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Employee:
    """Basic representation of an employee at the company."""

    name: str
    role: str
    vacation_days: int = 25

    def take_a_holiday(self, payout: bool) -> None:
        """Let the employee take a single holiday, or pay out 5 holidays."""
        if payout:
            # check whether self.vacation_days is less than 5
            if self.vacation_days < 5:
                raise ValueError(
                    f"You don't have enough holidays left over for a payout.\
                        Remaining holidays: {self.vacation_days}."
                )
            self.vacation_days -= 5
            print(f"Paying out a holiday. Holidays left: {self.vacation_days}")
        else:
            # check whether self.vacation_days is less than 1
            if self.vacation_days < 1:
                raise ValueError(
                    "You don't have any holidays left. Now back to work, you!"
                )
            self.vacation_days -= 1
            print("Have fun on your holiday. Don't forget to check your emails!")


@dataclass
class HourlyEmployee(Employee):
    hourly_rate: float = 50
    amount: int = 10


@dataclass
class SalariedEmployee(Employee):
    monthly_salary: float = 5000


@dataclass
class Freelancer(Employee):
    hourly_rate: float = 50
    amount: int = 10
    retainer: float = 1000


@dataclass
class Intern(Employee):
    monthly_salary: float = 1000


class Company:
    """Represents a company with employees."""

    def __init__(self) -> None:
        self.employees: list[Employee] = []

    def add_employee(self, employee: Employee) -> None:
        self.employees.append(employee)

    def find_managers(self) -> list[Employee]:
        return [e for e in self.employees if e.role == "manager"]

    def find_vice_presidents(self) -> list[Employee]:
        return [e for e in self.employees if e.role == "vice-president"]

    def find_support_staff(self) -> list[Employee]:
        return [e for e in self.employees if e.role == "support"]

    def pay_employee(self, employee: Employee) -> None:
        if isinstance(employee, SalariedEmployee):
            print(
                f"Paying employee {employee.name} a monthly salary of ${employee.monthly_salary}."
            )
        elif isinstance(employee, HourlyEmployee):
            print(
                f"Paying employee {employee.name} a hourly rate of \
                ${employee.hourly_rate} for {employee.amount} hours."
            )
        elif isinstance(employee, Freelancer):
            print(
                f"Paying freelancer {employee.name} a hourly rate of \
                ${employee.hourly_rate} for {employee.amount} hours."
            )
        elif isinstance(employee, Intern):
            print(
                f"Paying intern {employee.name} a monthly salary of ${employee.monthly_salary}."
            )


class Notification(ABC):
    """Abstract base class for notifications."""

    @abstractmethod
    def send(self, employee: Employee, message: str) -> None:
        pass


class EmailNotification(Notification):
    """Email notification implementation."""

    def send(self, employee: Employee, message: str) -> None:
        print(f"Sending email to {employee.name}: {message}")


class SMSNotification(Notification):
    """SMS notification implementation."""

    def send(self, employee: Employee, message: str) -> None:
        print(f"Sending SMS to {employee.name}: {message}")


class NotificationFactory:
    """Factory for creating notifications."""

    @staticmethod
    def get_notification(method: str) -> Notification:
        if method == "email":
            return EmailNotification()
        elif method == "sms":
            return SMSNotification()
        else:
            raise ValueError("Invalid notification method")


def main() -> None:
    """Main function."""

    company = Company()

    louis = SalariedEmployee(name="Louis", role="manager")
    company.add_employee(louis)
    company.add_employee(HourlyEmployee(name="Brenda", role="president"))
    company.add_employee(HourlyEmployee(name="Tim", role="support"))

    print(company.find_vice_presidents())
    print(company.find_managers())
    print(company.find_support_staff())
    company.pay_employee(company.employees[0])
    company.employees[0].take_a_holiday(False)

    notification = NotificationFactory.get_notification("email")
    notification.send(employee=louis, message="Your leave request is approved.")


if __name__ == "__main__":
    main()
