import unittest

from load_data import load_train_data, load_test_data, load_train_labels, load_test_labels


class TestDataLoadingFunctions(unittest.TestCase):

    def test_training_data_has_60_000_examples(self):
        self.assertEqual(len(load_train_data()), 60_000)

    def test_training_labels_has_60_000_examples(self):
        self.assertEqual(len(load_train_labels()), 60_000)

    def test_testing_data_has_10_000_examples(self):
        self.assertEqual(len(load_test_data()), 10_000)

    def test_testing_labels_has_10_000_examples(self):
        self.assertEqual(len(load_test_labels()), 10_000)


if __name__ == '__main__':
    unittest.main()
