"""
Employee class tests.
"""
import unittest

from employee import Employee

NAME: str = "Arjan"
EMPLOYEE_ID: int = 12345


class TestEmployeeComputePayout(unittest.TestCase):
    """Test the compute_payout method of the Employee class."""

    def test_employee_payout_returns_a_float(self):
        """Whether payout returns a float."""
        arjan = Employee(name=NAME, employee_id=EMPLOYEE_ID)
        self.assertIsInstance(arjan.compute_payout(), float)

    def test_employee_payout_no_commission_no_hours(self):
        """Whether payout is correctly computed in case of no commission and no hours worked."""
        arjan = Employee(name=NAME, employee_id=EMPLOYEE_ID)
        self.assertAlmostEqual(arjan.compute_payout(), 1000.0)

    def test_employee_payout_no_commission(self):
        """Whether payout is correctly computed in case of no commission and 10 hours worked."""
        arjan = Employee(name=NAME, employee_id=EMPLOYEE_ID, hours_worked=10)
        self.assertAlmostEqual(arjan.compute_payout(), 2000.0)

    def test_employee_payout_with_commission(self):
        """
        Whether payout is correctly computed in case of
        10 contracts landed and 10 hours worked.
        """
        arjan = Employee(
            name=NAME,
            employee_id=EMPLOYEE_ID,
            hours_worked=10.0,
            contracts_landed=10,
        )
        self.assertAlmostEqual(arjan.compute_payout(), 3000.0)

    def test_employee_payout_commission_disabled(self):
        """
        Whether payout is correctly computed in case of
        10 contracts landed and 10 hours worked,
        but commission is disabled.
        """
        arjan = Employee(
            name=NAME,
            employee_id=EMPLOYEE_ID,
            hours_worked=10.0,
            contracts_landed=10,
            commission=0.0,
        )
        self.assertAlmostEqual(arjan.compute_payout(), 2000.0)


if __name__ == "__main__":
    unittest.main()
