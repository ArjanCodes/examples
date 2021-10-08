"""
Employee class tests.
"""


import pytest
from hr.employee import Employee

NAME: str = "Arjan"
EMPLOYEE_ID: int = 12345


@pytest.fixture
def test_employee() -> Employee:
    return Employee(name=NAME, employee_id=EMPLOYEE_ID)


class TestEmployeeComputePayout:
    """Test the compute_payout method of the Employee class."""

    def test_employee_payout_returns_a_float(self, test_employee: Employee):
        """Whether payout returns a float."""
        assert isinstance(test_employee.compute_payout(), int)

    def test_employee_payout_no_commission_no_hours(self, test_employee: Employee):
        """Whether payout is correctly computed in case of no commission and no hours worked."""
        assert test_employee.compute_payout() == 100000

    def test_employee_payout_no_commission(self, test_employee: Employee):
        """Whether payout is correctly computed in case of no commission and 10 hours worked."""
        test_employee.hours_worked = 10.0
        assert test_employee.compute_payout() == 200000

    def test_employee_payout_with_commission(self, test_employee: Employee):
        """
        Whether payout is correctly computed in case of
        10 contracts landed and 10 hours worked.
        """
        test_employee.hours_worked = 10.0
        test_employee.contracts_landed = 10
        assert test_employee.compute_payout() == 300000

    def test_employee_payout_commission_disabled(self, test_employee: Employee):
        """
        Whether payout is correctly computed in case of
        10 contracts landed and 10 hours worked,
        but commission is disabled.
        """
        test_employee.hours_worked = 10.0
        test_employee.contracts_landed = 10
        test_employee.commission = 0
        assert test_employee.compute_payout() == 200000
