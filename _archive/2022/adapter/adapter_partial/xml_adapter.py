from typing import Any

from bs4 import BeautifulSoup


def get_from_bs(soup: BeautifulSoup, key: str, default: Any = None) -> Any | None:
    value = soup.find(key)
    if value:
        return value.get_text()
    return default
