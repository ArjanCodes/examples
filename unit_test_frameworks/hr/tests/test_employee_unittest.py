"""
Employee class tests.
"""
import unittest

from hr.employee import Employee

NAME: str = "Arjan"
EMPLOYEE_ID: int = 12345


class TestEmployeeComputePayout(unittest.TestCase):
    """Test the compute_payout method of the Employee class."""

    def setUp(self):
        """Set up test fixtures."""
        self.arjan = Employee(name=NAME, employee_id=EMPLOYEE_ID)

    def test_employee_payout_returns_a_float(self):
        """Whether payout returns a float."""
        self.assertIsInstance(self.arjan.compute_payout(), int)

    def test_employee_payout_no_commission_no_hours(self):
        """Whether payout is correctly computed in case of no commission and no hours worked."""
        self.assertEqual(self.arjan.compute_payout(), 100000)

    def test_employee_payout_negative_hours(self):
        self.arjan.hours_worked = -20
        self.assertRaises(ValueError, self.arjan.compute_payout)

    def test_employee_payout_no_commission(self):
        """Whether payout is correctly computed in case of no commission and 10 hours worked."""
        self.arjan.hours_worked = 10.0
        self.assertEqual(self.arjan.compute_payout(), 200000)

    def test_employee_payout_with_commission(self):
        """
        Whether payout is correctly computed in case of
        10 contracts landed and 10 hours worked.
        """
        self.arjan.hours_worked = 10.0
        self.arjan.contracts_landed = 10
        self.assertEqual(self.arjan.compute_payout(), 300000)

    def test_employee_payout_commission_disabled(self):
        """
        Whether payout is correctly computed in case of
        10 contracts landed and 10 hours worked,
        but commission is disabled.
        """
        self.arjan.hours_worked = 10.0
        self.arjan.contracts_landed = 10
        self.arjan.commission = 0

        self.assertEqual(self.arjan.compute_payout(), 200000)
