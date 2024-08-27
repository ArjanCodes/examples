# Function naming convention
# 1. Use lowercase letters
# 2. Separate words with underscores

# Public function


def public_function():
    pass


# Private function


def _private_function():
    pass


# Good name
# Name describes what the function does
def calculate_total_price(items: list[int], discount: int):
    if not items:
        return 0

    total_price = sum(items) - discount
    return max(total_price, 0)


# Bad name
# Does not say what the function does
def total(items: list[int], discount: int) -> int:
    if not items:
        return 0

    total_price = sum(items) - discount
    return max(total_price, 0)


# Bad name
# Do not include the return type in the name, the type hint is enough
def calculate_integer_total_price(items: list[int], discount: int) -> int:
    if not items:
        return 0

    total_price = sum(items) - discount
    return max(total_price, 0)
