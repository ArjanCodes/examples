from .employees.employee import Employee


def send_email(employee: Employee, message: str) -> None:
    print(f"Sending email to {employee.name}: {message}")


def send_sms(employee: Employee, message: str) -> None:
    print(f"Sending SMS to {employee.name}: {message}")
