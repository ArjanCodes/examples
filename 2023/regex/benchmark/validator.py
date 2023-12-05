import re

from timer import timer_decorator

@timer_decorator
def validate_email(regex: str, email: str):
    return re.match(regex, email)