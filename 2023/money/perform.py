import decimal
import timeit

import numpy as np

# Test numbers
INT_NUM = 12345
LARGE_INT_NUM = 12345678901234567890
NP_INT_NUM = np.int64(12345)
FLOAT_NUM = 12345.6789
LARGE_FLOAT_NUM = 12345678901234567890.1234567890
DECIMAL_NUM = decimal.Decimal("12345.6789")


# Test functions
def test_int():
    return INT_NUM * INT_NUM + INT_NUM - INT_NUM // INT_NUM


def test_large_int():
    return (
        LARGE_INT_NUM * LARGE_INT_NUM + LARGE_INT_NUM - LARGE_INT_NUM // LARGE_INT_NUM
    )


def test_float():
    return FLOAT_NUM * FLOAT_NUM + FLOAT_NUM - FLOAT_NUM // FLOAT_NUM


def test_large_float():
    return (
        LARGE_FLOAT_NUM * LARGE_FLOAT_NUM
        + LARGE_FLOAT_NUM
        - LARGE_FLOAT_NUM // LARGE_FLOAT_NUM
    )


def test_decimal():
    return DECIMAL_NUM * DECIMAL_NUM + DECIMAL_NUM - DECIMAL_NUM // DECIMAL_NUM


def test_numpy():
    return NP_INT_NUM * NP_INT_NUM + NP_INT_NUM - NP_INT_NUM // NP_INT_NUM


def main() -> None:
    # Time the functions
    int_time = timeit.timeit(test_int, number=1000000)
    large_int_time = timeit.timeit(test_large_int, number=1000000)
    float_time = timeit.timeit(test_float, number=1000000)
    large_float_time = timeit.timeit(test_large_float, number=1000000)
    decimal_time = timeit.timeit(test_decimal, number=1000000)
    numpy_time = timeit.timeit(test_numpy, number=1000000)

    print("Execution times (in seconds) for 1,000,000 operations:")
    print(f"Integer: {int_time:.6f}")
    print(f"Very Large Integer: {large_int_time:.6f}")
    print(f"Float: {float_time:.6f}")
    print(f"Very Large Float: {large_float_time:.6f}")
    print(f"Decimal: {decimal_time:.6f}")
    print(f"Numpy: {numpy_time:.6f}")


if __name__ == "__main__":
    main()
