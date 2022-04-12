from dataclasses import dataclass


@dataclass(frozen=True)
class BeautifulSoupJSONElement:
    value: str

    def get_text(self) -> str:
        return self.value


class BeautifulSoupJSONAdapter:
    def __init__(self, data: dict[str, str | int]):
        self.data = data

    def find(self, name: str) -> BeautifulSoupJSONElement:
        return BeautifulSoupJSONElement(str(self.data[name]))
