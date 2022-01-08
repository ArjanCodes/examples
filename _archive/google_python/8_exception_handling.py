import logging
import random


class MinimumPortError(Exception):
    def __init__(self, minimum: int):
        self.minimum = minimum
        self.message = f"Min. port must be at least 1024, not {self.minimum}"


def find_open_port(minimum: int) -> int:
    return random.randint(minimum, 9999)


def connect_to_next_port(minimum: int) -> int:
    if minimum < 1024:
        raise MinimumPortError(minimum)
    port = find_open_port(minimum)
    if not port:
        raise ConnectionError(
            f"Could not connect to service on port {minimum} or higher."
        )
    assert port >= minimum, f"Unexpected port {port} when minimum was {minimum}."
    return port


def main():
    logging.basicConfig(level=logging.INFO)

    port = 1200
    connect_to_next_port(port)
    logging.info(f"Connected to port {port}")


if __name__ == "__main__":
    main()
