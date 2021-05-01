import unittest
from io import StringIO
from unittest.mock import patch
from final import *

class Authorizer_SMS_TestCase(unittest.TestCase):

    def test_init_authorized(self):
        auth = Authorizer_SMS()
        self.assertFalse(auth.is_authorized())
    
    def test_code_decimal(self):
        auth = Authorizer_SMS()
        auth.generate_sms_code()
        self.assertTrue(auth.code.isdecimal())

    def test_authorize_success(self):
        auth = Authorizer_SMS()
        auth.generate_sms_code()
        with patch('builtins.input', return_value=auth.code):
            auth.authorize()
            self.assertTrue(auth.is_authorized())

    @patch('builtins.input', return_value="1234567")
    def test_authorize_fail(self, mocked_input):
        auth = Authorizer_SMS()
        auth.generate_sms_code()
        auth.authorize()
        self.assertFalse(auth.is_authorized())

class Authorizer_Robot_TestCase(unittest.TestCase):

    def test_init_authorized(self):
        auth = Authorizer_SMS()
        self.assertFalse(auth.is_authorized())

    def test_authorize_success(self):
        with patch('builtins.input', return_value="n"):
            auth = Authorizer_Robot()
            auth.authorize()
            self.assertTrue(auth.is_authorized())

    def test_authorize_success_uppercase(self):
        with patch('builtins.input', return_value="N"):
            auth = Authorizer_Robot()
            auth.authorize()
            self.assertTrue(auth.is_authorized())

    def test_authorize_fail(self):
        with patch('builtins.input', return_value="y"):
            auth = Authorizer_Robot()
            auth.authorize()
            self.assertFalse(auth.is_authorized())

class PaymentProcessor_TestCase(unittest.TestCase):

    def test_init(self):
        auth = Authorizer_Robot()
        p = PaymentProcessor(auth)
        self.assertEqual(p.authorizer, auth)

    def test_payment_success(self):
        with patch('sys.stdout', new=StringIO()) as mocked_output:
            auth = Authorizer_Robot()
            auth.authorized = True
            p = PaymentProcessor(auth)
            order_id = "abcdef"
            expected_out = f"Processing payment for order with id {order_id}"
            p.pay(order_id)
            self.assertEqual(mocked_output.getvalue().strip(), expected_out)

    def test_payment_fail(self):
        with self.assertRaises(Exception):
            auth = Authorizer_Robot()
            auth.authorized = False
            p = PaymentProcessor(auth)
            p.pay("abcdef")


if __name__ == '__main__':
    unittest.main()