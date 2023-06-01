from base64 import b64encode
from dataclasses import dataclass


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


def to_uri(s: str | int | bytes) -> URI | bool:
    if isinstance(s, str):
        s = s.encode()
    elif isinstance(s, int):
        s = str(s).encode()
    if len(s) < 2:
        return False
    return URI(
        scheme="data",
        authority="",
        path=f"text/plain;charset=us-ascii;base64,{b64encode(s).decode()}",
        query="",
        fragment="",
    )


def main() -> None:
    uri_data = input("Enter data to encode: ")
    uri = to_uri(uri_data)
    if uri:
        print(uri)
    else:
        print("Invalid data")


if __name__ == "__main__":
    main()
