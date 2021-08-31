import unittest

import torch

from load_data import load_train_data, load_test_data, load_train_labels, load_test_labels
from dataset import MNIST, get_train_dataloader

MAX_LOOPS: int = 5


class TestTestingMNIST(unittest.TestCase):

    def setUp(self):
        self.mnist = MNIST(load_test_data(), load_test_labels())

    def test_is_iterable(self):
        i = 0
        for _ in self.mnist:
            i += 1
            if i > MAX_LOOPS:
                break

    def test_yields_x_y_pairs(self):
        i = 0
        for x, y in self.mnist:
            i += 1
            if i > MAX_LOOPS:
                break

    def test_x_is_a_tensor(self):
        for i in range(MAX_LOOPS - 1):
            x, _ = self.mnist[i]
            with self.subTest(x=x):
                self.assertIsInstance(x, torch.Tensor)

    def test_x_are_float32(self):
        for i in range(MAX_LOOPS - 1):
            x, _ = self.mnist[i]
            with self.subTest(x=x):
                self.assertEqual(x.dtype, torch.float32)

    def test_x_has_3_dims(self):
        for i in range(MAX_LOOPS - 1):
            x, _ = self.mnist[i]
            with self.subTest(x=x):
                self.assertEqual(x.ndim, 3)

    def test_y_is_a_tensor(self):
        for i in range(MAX_LOOPS - 1):
            _, y = self.mnist[i]
            with self.subTest(y=y):
                self.assertIsInstance(y, torch.Tensor)

    def test_y_has_0_dim(self):
        for i in range(MAX_LOOPS - 1):
            _, y = self.mnist[i]
            with self.subTest(y=y):
                self.assertEqual(y.ndim, 0)

    def test_y_is_int32(self):
        for i in range(MAX_LOOPS - 1):
            _, y = self.mnist[i]
            with self.subTest(y=y):
                self.assertEqual(y.dtype, torch.long)


class TestTrainingMNIST(unittest.TestCase):

    def setUp(self):
        self.mnist = MNIST(load_train_data(), load_train_labels())

    def test_is_iterable(self):
        i = 0
        for _ in self.mnist:
            i += 1
            if i > MAX_LOOPS:
                break

    def test_yields_x_y_pairs(self):
        i = 0
        for x, y in self.mnist:
            i += 1
            if i > MAX_LOOPS:
                break

    def test_x_is_a_tensor(self):
        for i in range(MAX_LOOPS - 1):
            x, _ = self.mnist[i]
            with self.subTest(x=x):
                self.assertIsInstance(x, torch.Tensor)

    def test_x_are_float32(self):
        for i in range(MAX_LOOPS - 1):
            x, _ = self.mnist[i]
            with self.subTest(x=x):
                self.assertEqual(x.dtype, torch.float32)

    def test_x_has_3_dims(self):
        for i in range(MAX_LOOPS - 1):
            x, _ = self.mnist[i]
            with self.subTest(x=x):
                self.assertEqual(x.ndim, 3)

    def test_y_is_a_tensor(self):
        for i in range(MAX_LOOPS - 1):
            _, y = self.mnist[i]
            with self.subTest(y=y):
                self.assertIsInstance(y, torch.Tensor)

    def test_y_has_0_dim(self):
        for i in range(MAX_LOOPS - 1):
            _, y = self.mnist[i]
            with self.subTest(y=y):
                self.assertEqual(y.ndim, 0)

    def test_y_is_int32(self):
        for i in range(MAX_LOOPS - 1):
            _, y = self.mnist[i]
            with self.subTest(y=y):
                self.assertEqual(y.dtype, torch.long)


class TestGetTrainDataloader(unittest.TestCase):

    def test_is_iterable(self):
        train_loader = get_train_dataloader(batch_size=1)
        i = 0
        for x, y in train_loader:
            i += 1
            if i > MAX_LOOPS:
                break

    def test_batch_size_equals_5(self):
        train_loader = get_train_dataloader(batch_size=5)
        self.assertEqual(train_loader.batch_size, 5)

    def test_x_is_size_7x1x28x28(self):
        train_loader = get_train_dataloader(batch_size=7)
        x, _ = next(iter(train_loader))
        self.assertEqual(x.shape, torch.Size((7, 1, 28, 28)))

    def test_y_is_size_13(self):
        train_loader = get_train_dataloader(batch_size=13)
        _, y = next(iter(train_loader))
        self.assertEqual(y.shape, torch.Size((13,)))


if __name__ == '__main__':
    unittest.main()
