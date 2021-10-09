"""
Employee class tests.
"""


import pytest
from hr.employee import DealBasedCommission, Employee, HourlyContract

NAME: str = "Arjan"
EMPLOYEE_ID: int = 12345


@pytest.fixture
def test_employee() -> Employee:
    return Employee(name=NAME, id=EMPLOYEE_ID)


class TestEmployeeComputePayout:
    """Test the compute_payout method of the Employee class."""

    def test_employee_payout_returns_a_float(self, test_employee: Employee):
        """Whether payout returns a float."""
        assert isinstance(test_employee.compute_pay(), int)

    def test_employee_payout_no_commission_no_hours(self, test_employee: Employee):
        """Whether payout is correctly computed in case of no commission and no hours worked."""
        assert test_employee.compute_pay() == 0

    def test_employee_payout_no_commission(self, test_employee: Employee):
        """Whether payout is correctly computed in case of no commission and 10 hours worked."""
        test_employee.add_payment_source(
            HourlyContract(hourly_rate=10000, hours_worked=10)
        )

        assert test_employee.compute_pay() == 200000

    def test_employee_payout_with_commission(self, test_employee: Employee):
        """
        Whether payout is correctly computed in case of
        10 deals landed and 10 hours worked.
        """
        test_employee.add_payment_source(
            HourlyContract(hourly_rate=10000, hours_worked=10)
        )
        test_employee.add_payment_source(DealBasedCommission(deals_landed=10))
        assert test_employee.compute_pay() == 300000
