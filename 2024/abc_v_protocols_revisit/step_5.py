from typing import Protocol
from abc import ABC, abstractmethod
from pickle import dumps as pickle_dumps, loads as pickle_loads
from json import dumps as json_dumps, loads as json_loads


class SerializedFileHandler(ABC):
    def __init__(self, filename):
        self.filename = filename

    @abstractmethod
    def serialize(self, data):
        pass

    @abstractmethod
    def deserialize(self, data):
        pass

    def write(self, data):
        with open(self.filename, 'wb') as file:
            file.write(self.serialize(data))

    def read(self):
        with open(self.filename, 'rb') as file:
            return self.deserialize(file.read())


class PickleHandler(SerializedFileHandler):
    def serialize(self, data):
        return pickle_dumps(data)

    def deserialize(self, data):
        return pickle_loads(data)


class JSONHandler(SerializedFileHandler):
    def serialize(self, data):
        return json_dumps(data).encode()

    def deserialize(self, data):
        return json_loads(data.decode())


class Writable(Protocol):
    def write(self, data: dict) -> None:
        """This method should write dictionary data."""


class Readable(Protocol):
    def read(self) -> dict:
        """This method should return a dictionary."""


def write(handler: Writable, data: dict) -> None:
    handler.write(data)


def read(handler: Readable) -> dict:
    return handler.read()


def main():
    data = {'name': 'John Doe', 'age': 30}
    pickle_writer = PickleHandler('../data.pkl')
    write(pickle_writer, data)
    print(read(pickle_writer))

    json_writer = JSONHandler('../data.json')
    write(json_writer, data)
    print(read(json_writer))

    assert isinstance(pickle_writer, Writable)
    assert isinstance(json_writer, Readable)


if __name__ == '__main__':
    main()
