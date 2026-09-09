"""A deliberately small CPU-bound target for profiling.sampling (Tachyon)."""


def count_primes(limit: int) -> int:
    count = 0
    for candidate in range(2, limit):
        for divisor in range(2, int(candidate**0.5) + 1):
            if candidate % divisor == 0:
                break
        else:
            count += 1
    return count


def main() -> None:
    print(f"primes below 100,000: {count_primes(100_000)}")


if __name__ == "__main__":
    main()
