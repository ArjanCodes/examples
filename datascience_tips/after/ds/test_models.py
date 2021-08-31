import unittest

import torch

from models import ConvNet, LinearNet


class TestConvNet(unittest.TestCase):

    def setUp(self):
        self.model = ConvNet()

    def test_model_accepts_input_shape_1x1x28x28(self):
        test_tensor = torch.randn((1, 1, 28, 28))
        _ = self.model(test_tensor)

    def test_model_accepts_input_shape_10x1x28x28(self):
        test_tensor = torch.randn((10, 1, 28, 28))
        _ = self.model(test_tensor)

    def test_model_accepts_input_shape_100x1x28x28(self):
        test_tensor = torch.randn((100, 1, 28, 28))
        _ = self.model(test_tensor)

    def test_model_outputs_1x10(self):
        test_tensor = torch.randn((1, 1, 28, 28))
        out = self.model(test_tensor)
        self.assertEqual(torch.Size((1, 10)), out.shape)

    def test_model_outputs_10x10(self):
        test_tensor = torch.randn((10, 1, 28, 28))
        out = self.model(test_tensor)
        self.assertEqual(torch.Size((10, 10)), out.shape)

    def test_model_outputs_100x10(self):
        test_tensor = torch.randn((100, 1, 28, 28))
        out = self.model(test_tensor)
        self.assertEqual(torch.Size((100, 10)), out.shape)


class TestLinearNet(unittest.TestCase):

    def setUp(self):
        self.model = LinearNet()

    def test_accepts_tensor_1x1x28x28(self):
        test_tensor = torch.randn((1, 1, 28, 28))
        _ = self.model(test_tensor)

    def test_accepts_tensor_10x1x28x28(self):
        test_tensor = torch.randn((10, 1, 28, 28))
        _ = self.model(test_tensor)

    def test_accepts_tensor_73x1x28x28(self):
        test_tensor = torch.randn((73, 1, 28, 28))
        _ = self.model(test_tensor)

    def test_output_is_shape_1x10(self):
        test_tensor = torch.randn((1, 1, 28, 28))
        out = self.model(test_tensor)
        self.assertEqual(out.shape, torch.Size((1, 10)))


if __name__ == '__main__':
    unittest.main()
