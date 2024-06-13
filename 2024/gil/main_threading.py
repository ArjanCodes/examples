from threading import Thread


def count_up(name: str, n: int):
    for i in range(n):
        print(f"{name}: {i}")


def main() -> None:
    threads: list[Thread] = []
    for i in range(5):
        t = Thread(target=count_up, args=(i, 5))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

    print("Execution Completed")


if __name__ == "__main__":
    main()
