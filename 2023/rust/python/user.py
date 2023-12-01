# Storing Data + Implementations

class User:
    def __init__(self, name, age):
        self.name = name
        self.email = name + '@arjancodes.com'
    
    def send_email(self, message):
        print(f'Sent {message} to {self.email}')