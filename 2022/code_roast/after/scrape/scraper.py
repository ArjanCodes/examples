from dataclasses import dataclass
from typing import Protocol


@dataclass
class ScrapeResult:
    DOI: str
    wordscore: int
    frequency: list[tuple[str, int]]
    study_design: list[tuple[str, int]]


class Scraper(Protocol):
    def scrape(self, search_text: str) -> ScrapeResult: ...
