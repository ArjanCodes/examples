import unittest

from utils import increment_experiment_number, is_first_experiment


class TestIsFirstExperiment(unittest.TestCase):

    def test_returns_true_for_empty_list(self):
        self.assertTrue(is_first_experiment([]))

    def test_returns_false_for_non_empty_list(self):
        self.assertFalse(is_first_experiment([0]))


class TestIncrementExperimentNumber(unittest.TestCase):

    def test_increments_from_7_to_8(self):
        self.assertEqual(increment_experiment_number([1, 7]), '8')

    def test_increments_from_0_to_1(self):
        self.assertEqual(increment_experiment_number([0, -1]), '1')


if __name__ == '__main__':
    unittest.main()
