import concurrent.futures


def count_up(name: str, n: int):
    for i in range(n):
        print(f"{name}: {i}")


def main() -> None:
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(count_up, str(i), 5) for i in range(5)]

        for future in concurrent.futures.as_completed(futures):
            future.result()  # We don't need the result here, but this ensures any exceptions are raised

    print("Execution Completed")


if __name__ == "__main__":
    main()
