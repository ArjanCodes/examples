from ops.company.company import Company
from ops.employees.types.hourly import HourlyEmployee
from ops.employees.types.salaried import SalariedEmployee
from ops.notification import send_email


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
    company.pay_employee(louis)
    louis.take_single_holiday()

    send_email(employee=louis, message="Your leave request is approved.")


if __name__ == "__main__":
    main()
