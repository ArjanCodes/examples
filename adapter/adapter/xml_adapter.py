from typing import Any

from bs4 import BeautifulSoup


class XMLAdapter:
    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup

    def get(self, key: str) -> Any | None:
        value = self.soup.find(key)
        if value:
            return value.get_text()
        return None


# Below is what you would need to do for a class adapter
# But it leads to a problem, because BeautifulSoup already has
# a get method with a different signature.
# This is exactly why I recommend avoiding class adapters.

# class XMLAdapter(BeautifulSoup):
#    def get(self, key: str) -> Any | None:
#        value = self.find(key)
#        if value:
#            return value.get_text()
#        return None
