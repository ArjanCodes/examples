from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from urllib.parse import urlparse


@dataclass(frozen=True)
class Endpoint:
    url: str

    @cached_property
    def parsed(self):
        # cached_property works on normal classes; frozen dataclass is fine because
        # cached_property stores on the instance via object.__setattr__ internally.
        return urlparse(self.url)

    @property
    def host(self) -> str:
        return self.parsed.hostname or ""

    @property
    def is_https(self) -> bool:
        return self.parsed.scheme == "https"


def main() -> None:
    e = Endpoint("https://arjan.codes/designguide")
    print(e.host)
    print(e.is_https)
    print(e.parsed)  # computed once, then cached


if __name__ == "__main__":
    main()
