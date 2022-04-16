from typing import Any

from bs4 import BeautifulSoup


def get_from_bs(soup: BeautifulSoup, key: str) -> Any | None:
    value = soup.find(key)
    if value:
        return value.get_text()
    return None
