from ops.employees.employee import Employee
from ops.notification import send_email


def test_send_email(capsys):
    employee = Employee("Alice", "manager")
    message = "Hello, Alice!"
    send_email(employee, message)
    captured = capsys.readouterr()
    assert captured.out == f"Sending email to Alice: {message}\n"
