from functools import reduce


def to_ascii_codes(inp: str) -> list[int]:
    return [ord(c) for c in inp]


def from_ascii_codes(inp: list[int]) -> str:
    return reduce(lambda x, y: x + chr(y), inp, "")
