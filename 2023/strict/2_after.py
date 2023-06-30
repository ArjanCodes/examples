from base64 import b64encode
from dataclasses import dataclass


@dataclass
class URITooShortError(Exception):
    uri_data: str

    def __str__(self) -> str:
        return f"URI data must be at least 2 characters long, but was {len(self.uri_data)}."


@dataclass
class URI:
    scheme: str
    authority: str
    path: str
    query: str
    fragment: str

    def __str__(self) -> str:
        return (
            f"{self.scheme}://{self.authority}{self.path}?{self.query}#{self.fragment}"
        )


def to_uri_from_int(s: int) -> URI:
    return to_uri(str(s).encode())


def to_uri_from_string(s: str) -> URI:
    return to_uri(s.encode())


def to_uri(s: bytes) -> URI:
    if len(s) < 2:
        raise URITooShortError(s)
    return URI(
        scheme="data",
        authority="",
        path=f"text/plain;charset=us-ascii;base64,{b64encode(s).decode()}",
        query="",
        fragment="",
    )


def main() -> None:
    uri_data = input("Enter data to encode: ")
    uri = to_uri_from_string(uri_data)
    print(uri)


if __name__ == "__main__":
    main()
