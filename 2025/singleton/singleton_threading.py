from threading import Thread

from singleton import Singleton


class Unsafe(metaclass=Singleton):
    def __init__(self):
        print("Initializing...")


def main() -> None:
    threads = [Thread(target=Unsafe) for _ in range(20)]
    [t.start() for t in threads]
    [t.join() for t in threads]


if __name__ == "__main__":
    main()
