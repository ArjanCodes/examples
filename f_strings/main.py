import datetime
from dataclasses import dataclass


@dataclass
class User:
    first_name: str
    last_name: str

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


def main():

    user = User("Elon", "Musk")
    print(f"User: {user}.")
    print(f"Raw user: {user!r}.")
    print(f"Raw user (alternative): {repr(user)}.")
    greet = "Hi"
    value = 42

    number = 800

    # printing variable names alongside their values
    x = 10
    y = 25
    print(f"x={x}, y={y}")
    print(f"{x=}, {y=}")  # Better! (3.8+)
    # x=10, y=25
    # This feature is called “debugging” and can be applied
    # in combination with other modifiers. It also preserves
    # whitespaces, so f"{x = }" and f"{x=}" will produce different strings.

    # Hexadecimal
    print(f"{number:x}")

    # Ocatal
    print(f"{number:o}")

    # Scientific
    print(f"{number:e}")

    # adding zeroes to the left
    print(f"The value is {value:06}")

    # add padding to the left
    for number in range(5, 15):
        print(f"The number is {number:4}")

    # Adding spaces to the left
    print(f"{greet:>10}")

    # Various alignment options
    print(f"{greet:_^10}")
    print(f"{greet:_<10}")
    print(f"{greet:_>10}")

    print(f"{3.4:10}")  # numbers are right aligned
    print(f"{3820.45:2}")  # value can be larger than the width

    print(f"{100.345736:.2f}")  # .2f is the number of decimal places

    print(f"{1000000:,.2f}")  # grouping thousands
    print(f"{1000000:_.2f}")  # grouping thousands

    print(f"{0.34576:%}")  # percentage
    print(f"{0.34576:.2%}")  # percentage with precision

    # date/time formatting
    today = datetime.datetime.today()
    print(f"{today:%y-%m-%d}")
    # 2022-03-11
    print(f"{today:%Y}")
    # 2022
    print(f"Today is a {today:%A}")  # full weekday name
    print(f"The date is {today:%A, %B %d, %Y}")

    # printing braces
    print(f"{{'Single Braces'}}")
    print(f"{{{{'This will print Double Braces'}}}}")

    # printing dictionary items (combining double and single quotes)
    details = {"name": "saral", "age": 30}
    print(f"Name: {details['name']}, Age: {details['age']}")

    # raw strings
    name = "Fred"
    print(f"He said his name is {name!r}.")

    # multiline strings
    name = "Arjan"
    country = "The Netherlands"
    channel = "ArjanCodes"
    sentence = (
        f"Hi, my name is {name}. "
        f"I am from a beautiful country called {country}. "
        f"I run a YouTube channel called {channel}."
    )
    print(sentence)

    # comments in f-strings are not allowed
    # f"Eric is {2 * 37 #Oh my!}." - will result in a SyntaxError


if __name__ == "__main__":
    main()
