import re
import time
import json

from timer import timer_decorator

# Specify the file path
OUTPUT_FILE_PATH = "output.json"
EMAIL_REGEX_BAD = r"^([a-zA-Z0-9])(([\-.]|[_]+)?([a-zA-Z0-9]+))*(@){1}[a-z0-9]+[.]{1}(([a-z]{2,3})|([a-z]{2,3}[.]{1}[a-z]{2,3}))$"
EMAIL_REGEX_GOOD = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
EMAIL_REGEX_GOOD_2 = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"


@timer_decorator
def validate_email(regex: str, email: str):
    return re.match(regex, email)


lengths = [i for i in range(1, 30)]

evil_strings = ["".join(["a" for _i in range(length)]) for length in lengths]

regexes: list[tuple[str, str]] = [("evil_pattern", EMAIL_REGEX_BAD), ("good_pattern_0", EMAIL_REGEX_GOOD), ("good_pattern_1", EMAIL_REGEX_GOOD_2)]

data = {}

for key, regex in regexes:
    data[key] = {"pattern": regex}

    for evil_string in evil_strings:
        start_time = time.time()

        validate_email(regex, evil_string)
        end_time = time.time()

        elapsed_time = end_time - start_time

        length_of_string = len(evil_string)
        data[key][length_of_string] =  elapsed_time

with open(OUTPUT_FILE_PATH, "w") as json_file:
    json.dump(data, json_file)
