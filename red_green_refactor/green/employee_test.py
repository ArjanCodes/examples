"""
Employee class tests.
"""
import unittest

from employee import Employee


class TestEmployeeMethods(unittest.TestCase):
    """Test the methods of the Employee class."""

    def test_employee_init(self):
        """Whether the employee is properly initialized."""
        arjan = Employee(name="Arjan", _id=12345)
        self.assertEqual(arjan.has_commission, True)

    def test_employee_payout_no_commission_no_hours(self):
        """Whether payout is correctly computed in case of no commission and no hours worked."""
        arjan = Employee(name="Arjan", _id=12345)
        self.assertEqual(arjan.compute_payout(), arjan.employer_cost)

    def test_employee_payout_no_commission(self):
        """Whether payout is correctly computed in case of no commission and 10 hours worked."""
        arjan = Employee(name="Arjan", _id=12345, hours_worked=10)
        self.assertEqual(arjan.compute_payout(), arjan.employer_cost + 1000.0)

    def test_employee_payout_with_commission(self):
        """
        Whether payout is correctly computed in case of
        10 contracts landed and 10 hours worked.
        """
        arjan = Employee(
            name="Arjan",
            _id=12345,
            hours_worked=10,
            contracts_landed=10,
        )
        self.assertEqual(arjan.compute_payout(), arjan.employer_cost + 2000.0)

    def test_employee_payout_commission_disabled(self):
        """
        Whether payout is correctly computed in case of
        10 contracts landed and 10 hours worked,
        but commission is disabled.
        """
        arjan = Employee(
            name="Arjan",
            _id=12345,
            hours_worked=10,
            contracts_landed=10,
            has_commission=False,
        )
        self.assertEqual(arjan.compute_payout(), arjan.employer_cost + 1000.0)


if __name__ == "__main__":
    unittest.main()
