from typing import Protocol, runtime_checkable
import io


@runtime_checkable
class Writable(Protocol):
    def write(self, data: dict) -> None:
        """This method should write dictionary data."""


def main():
    io_writer = io.BytesIO()

    assert isinstance(io_writer, Writable)

    # io_writer.write({'name': 'John Doe', 'age': 30})


if __name__ == "__main__":
    main()
