import multiprocessing


def count_up(name: str, n: int):
    for i in range(n):
        print(f"{name}: {i}")


def main() -> None:
    jobs: list[multiprocessing.Process] = []
    for i in range(5):
        p = multiprocessing.Process(target=count_up, args=(i, 5))
        jobs.append(p)
        p.start()

    for job in jobs:
        job.join()

    print("Execution Completed")


if __name__ == "__main__":
    main()
