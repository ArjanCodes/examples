import pytest
import sys

# Function we want to test
def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


# Parametrized test: tests multiple inputs in one go
@pytest.mark.parametrize("n, expected", [
    (2, True),
    (3, True),
    (4, False),
    (17, True),
    (18, False),
    (1, False),
    (0, False),
    (-5, False),
])
def test_is_prime(n: int, expected: bool) -> None:
    assert is_prime(n) == expected


# Optional: run pytest programmatically from the same file
if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))