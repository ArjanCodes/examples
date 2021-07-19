"""
Employee class tests.
"""
import unittest

from employee import Employee

NAME: str = "Arjan"
EMPLOYEE_ID: int = 12345


class TestEmployeeComputePayout(unittest.TestCase):
    """Test the compute_payout method of the Employee class."""

    def setUp(self):
        """Create Employee used for testing. [DON'T REUSE INSTANCES IN DIFFERENT TESTS!]"""
        self.employee_to_test = Employee(name=NAME, employee_id=EMPLOYEE_ID)

    def test_employee_attributes(self):
        """Ensure Employee attributes are as expected. [NOT NEEDED!]"""
        expected_attributes = {
            "name": NAME,
            "employee_id": EMPLOYEE_ID,
            "pay_rate": 100.0,
            "hours_worked": 0.0,
            "employer_cost": 1000.0,
            "commission": 100.0,
            "contracts_landed": 0,
        }
        for key, value in expected_attributes.items():
            value_to_test = getattr(self.employee_to_test, key)
            with self.subTest(attribute=key, expected=value, actual=value_to_test):
                self.assertEqual(value, value_to_test)

    def compute_payout(self, employee: Employee) -> float:
        """Compute the expected payout for an employee."""
        payout = employee.pay_rate * employee.hours_worked + employee.employer_cost
        if employee.commission > 0:
            payout += employee.commission * employee.contracts_landed
        return payout

    def test_employee_payout_returns_a_float(self):
        """Whether payout returns a float."""
        self.assertIsInstance(self.employee_to_test.compute_payout(), float)

    def test_employee_payout_no_commission_no_hours(self):
        """Whether payout is correctly computed in case of no commission and no hours worked.
        [NO, YOU'RE CHECKING NOW WHETHER COPYING THE IMPLEMENTATION WORKS. USE CONSTANTS INSTEAD.]"""
        self.assertAlmostEqual(
            self.employee_to_test.compute_payout(),
            self.compute_payout(self.employee_to_test),
        )

    def test_employee_payout_no_commission(self):
        """Whether payout is correctly computed in case of no commission and 10 hours worked."""
        self.employee_to_test.hours_worked = 10.0
        self.assertAlmostEqual(self.employee_to_test.compute_payout(), 2000.0)

    def test_employee_payout_with_commission(self):
        """
        Whether payout is correctly computed in case of
        10 contracts landed and 10 hours worked.
        """
        print(self.employee_to_test)
        self.employee_to_test.hours_worked = 10.0
        self.employee_to_test.contracts_landed = 10
        self.assertAlmostEqual(self.employee_to_test.compute_payout(), 3000.0)

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
