import time


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def count_primes(limit):
    return sum(1 for i in range(2, limit + 1) if is_prime(i))


def main() -> None:
    n = 1_000_000  # Define a large number
    start_time = time.time()
    result = count_primes(n)
    end_time = time.time()
    print(f"Number of primes: {result}")
    print(f"Execution time (Python): {end_time - start_time:.4f} seconds")


if __name__ == "__main__":
    main()
