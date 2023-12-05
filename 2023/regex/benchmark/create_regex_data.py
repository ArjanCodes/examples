import json
import time
from expressions import EMAIL_REGEX_BAD, EMAIL_REGEX_GOOD, EMAIL_REGEX_GOOD_2
from validator import validate_email

OUTPUT_FILE_PATH = "output.json"

lengths = [i for i in range(1, 30)]

EVIL_STRINGS = ["".join(["a" for _i in range(length)]) for length in lengths]

regexes: list[tuple[str, str]] = [
    ("evil_pattern", EMAIL_REGEX_BAD),
    ("good_pattern_0", EMAIL_REGEX_GOOD),
    ("good_pattern_1", EMAIL_REGEX_GOOD_2),
]

data = {}

for key, regex in regexes:
    data[key] = {"pattern": regex}

    for evil_string in EVIL_STRINGS:
        start_time = time.time()

        validate_email(regex, evil_string)
        end_time = time.time()

        elapsed_time = end_time - start_time

        length_of_string = len(evil_string)
        data[key][length_of_string] = elapsed_time

with open(OUTPUT_FILE_PATH, "w") as json_file:
    json.dump(data, json_file)
