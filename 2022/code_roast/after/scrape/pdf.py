import re
from os import path
from typing import Any

import pdfplumber
from nltk import FreqDist
from nltk.corpus import names, stopwords
from nltk.tokenize import word_tokenize

from scrape.scraper import Scraper, ScrapeResult

STOP_WORDS: set[str] = set(stopwords.words("english"))

NAME_WORDS: set[str] = set(names.words())


def guess_doi(path_name: str) -> str:
    basename = path.basename(path_name)
    doi = basename[7:-4]
    return f"{doi[:7]}/{doi[7:]}"


def compute_filtered_tokens(text: list[str]) -> set[str]:
    """Takes a lowercase string, now removed of its non-alphanumeric characters.
    It returns (as a list comprehension) a parsed and tokenized
    version of the text, with stopwords and names removed.
    """
    word_tokens = word_tokenize("\n".join(text))
    return set([w for w in word_tokens if not w in STOP_WORDS and NAME_WORDS])


def most_common_words(word_set: set[str], n: int) -> list[tuple[str, int]]:
    return FreqDist(word_set).most_common(n)


class PDFScraper(Scraper):
    def __init__(self, research_words: str, bycatch_words: str, target_words: str):
        with open(research_words, encoding="utf8") as f:
            self.research_words = set(f.readlines())
        with open(bycatch_words, encoding="utf8") as f:
            self.bycatch_words = set(f.readlines())
        with open(target_words, encoding="utf8") as f:
            self.target_words = set(f.readlines())

    def scrape(self, search_text: str) -> ScrapeResult:
        preprints: list[str] = []
        with pdfplumber.open(search_text) as study:
            pages: list[Any] = study.pages
            n = len(pages)
            pages_to_check: list[Any] = [page for page in pages][:n]
            for page_number, page in enumerate(pages_to_check):
                page: str = pages[page_number].extract_text(
                    x_tolerance=3, y_tolerance=3
                )
                print(
                    f"[sciscraper]: Processing Page {page_number} of {n-1} | {search_text}...",
                    end="\r",
                )
                preprints.append(
                    page
                )  # Each page's string gets appended to preprint []

            manuscripts = [str(preprint).strip().lower() for preprint in preprints]
            # The preprints are stripped of extraneous characters and all made lower case.
            postprints = [re.sub(r"\W+", " ", manuscript) for manuscript in manuscripts]
            # The ensuing manuscripts are stripped of lingering whitespace and non-alphanumeric characters.
            all_words = compute_filtered_tokens(postprints)
            research_word_overlap = self.research_words.intersection(all_words)

            doi = guess_doi(search_text)

            target_intersection = self.target_words.intersection(all_words)
            bycatch_intersection = self.bycatch_words.intersection(all_words)
            wordscore = len(target_intersection) - len(bycatch_intersection)
            frequency = most_common_words(all_words, 5)
            study_design = most_common_words(research_word_overlap, 3)

            return ScrapeResult(
                doi,
                wordscore,
                frequency,
                study_design,
            )
