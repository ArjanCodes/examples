from toolz import compose

strip_upper = compose(str.strip, str.upper)
print(strip_upper("  hello  "))  # -> "HELLO"
