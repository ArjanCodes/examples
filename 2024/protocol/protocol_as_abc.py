from typing import Protocol
import abc


class Writable(Protocol):
    @abc.abstractmethod
    def write(self, data: dict) -> None:
        """This method should write dictionary data."""


class Readable(Protocol):
    @abc.abstractmethod
    def read(self) -> dict:
        """This method should return a dictionary."""


class ReadWritable(Readable, Writable):
    def __str__(self):
        return f"{self.__class__.__name__}()"

    def write(self, data: dict) -> None:
        """Write some data."""


def main():
    data = {"name": "John Doe", "age": 30}
    handlers = ReadWritable()
    handlers.write(data)
    print(handlers.read())


if __name__ == "__main__":
    main()
