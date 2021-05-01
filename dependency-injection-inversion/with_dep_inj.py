import string
import random
from abc import ABC, abstractmethod

class Authorizer_SMS:

    def __init__(self):
        self.authorized = False
        self.code = None

    def generate_sms_code(self):
        self.code = ''.join(random.choices(string.digits, k=6))

    def authorize(self):
        code = input("Enter SMS code: ")
        self.authorized = code == self.code

    def is_authorized(self) -> bool:
        return self.authorized

class PaymentProcessor:

    def __init__(self, authorizer: Authorizer_SMS):
        self.authorizer = authorizer
    
    def pay(self, order_id):
        self.authorizer.generate_sms_code()
        if not self.authorizer.is_authorized():
            raise Exception("Not authorized")
        print(f"Processing payment for order with id {order_id}")
