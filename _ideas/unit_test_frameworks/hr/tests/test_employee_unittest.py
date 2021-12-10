"""
Employee class tests.
"""
import unittest
from unittest import mock

from hr.employee import DealBasedCommission, Employee, HourlyContract

NAME: str = "Arjan"
EMPLOYEE_ID: int = 12345


class TestEmployeeComputePayout(unittest.TestCase):
    """Test the compute_pay method of the Employee class."""

    def setUp(self):
        """Set up test fixtures."""
        self.arjan = Employee(name=NAME, id=EMPLOYEE_ID)

    def test_employee_payout_returns_an_int(self):
        """Whether payout returns an int."""
        self.assertIsInstance(self.arjan.compute_pay(), int)

    def test_employee_payout_no_commission_no_hours(self):
        """Whether payout is correctly computed in case of no commission and no hours worked."""
        self.assertEqual(self.arjan.compute_pay(), 0)

    def test_employee_payout_no_commission(self):
        """Whether payout is correctly computed in case of no commission and 10 hours worked."""
        self.arjan.add_payment_source(
            HourlyContract(hourly_rate=100_00, hours_worked=10)
        )
        self.assertEqual(self.arjan.compute_pay(), 2000_00)

    def test_employee_payout_with_commission(self):
        """
        Whether payout is correctly computed in case of
        10 deals landed and 10 hours worked.
        """
        self.arjan.add_payment_source(
            HourlyContract(hourly_rate=10000, hours_worked=10)
        )
        self.arjan.add_payment_source(DealBasedCommission(deals_landed=10))
        self.assertEqual(self.arjan.compute_pay(), 3000_00)

    def test_source_method_called(self):
        """
        Whether payout is correctly computed in case of
        10 deals landed and 10 hours worked.
        """
        contract = HourlyContract(hourly_rate=10000, hours_worked=10)
        contract.compute_pay = mock.MagicMock(return_value=1000_00)
        self.arjan.add_payment_source(contract)
        self.arjan.compute_pay()
        contract.compute_pay.assert_called_once()
