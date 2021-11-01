import re

import pdfplumber
from nltk import FreqDist
from nltk.corpus import names, stopwords
from nltk.tokenize import word_tokenize

TARGET_WORDS = [
    "prosocial",
    "design",
    "intervention",
    "reddit",
    "humane",
    "social media",
    "user experience",
    "nudge",
    "choice architecture",
    "user interface",
    "misinformation",
    "disinformation",
    "Trump",
    "conspiracy",
    "dysinformation",
    "users",
    "Thaler",
    "Sunstein",
    "boost",
]

BYCATCH_WORDS = [
    "psychology",
    "pediatric",
    "pediatry",
    "autism",
    "mental",
    "medical",
    "oxytocin",
    "adolescence",
    "infant",
    "health",
    "wellness",
    "child",
    "care",
    "mindfulness",
]


def compute_intersection(list1: list[str], list2: list[str]) -> list[str]:
    return [value for value in list1 if value in list2]


class PDFScrape:
    """The PDFScrape class takes the provided string from a prior list
    comprehension of PDF files in a directory. From each pdf file, it parses the document
    and returns metrics about its composition and relevance.
    """

    def download(self, search_text: str) -> dict:
        self.search_text = search_text
        self.preprints = []
        with pdfplumber.open(self.search_text) as self.study:
            self.n = len(self.study.pages)
            self.pages_to_check = [page for page in self.study.pages][: self.n]
            for page_number, page in enumerate(self.pages_to_check):
                page = self.study.pages[page_number].extract_text(
                    x_tolerance=3, y_tolerance=3
                )
                print(
                    f"[sciscraper]: Processing Page {page_number} of {self.n-1} | {search_text}...",
                    end="\r",
                )
                self.preprints.append(
                    page
                )  # Each page's string gets appended to preprint []

            self.manuscripts = [
                str(preprint).strip().lower() for preprint in self.preprints
            ]
            # The preprints are stripped of extraneous characters and all made lower case.
            self.postprints = [
                re.sub(r"\W+", " ", manuscript) for manuscript in self.manuscripts
            ]
            # The ensuing manuscripts are stripped of lingering whitespace and non-alphanumeric characters.
            self.all_words = self.get_tokens()
            self.research_word_overlap = self.get_research_words()
            return self.get_data_entry()

    def get_tokens(self) -> list:
        """Takes a lowercase string, now removed of its non-alphanumeric characters.
        It returns (as a list comprehension) a parsed and tokenized
        version of the postprint, with stopwords and names removed.
        """
        self.stop_words = set(stopwords.words("english"))
        self.name_words = set(names.words())
        self.word_tokens = word_tokenize(str(self.postprints))
        return [
            w for w in self.word_tokens if not w in self.stop_words and self.name_words
        ]  # Filters out the stopwords

    def get_bycatch_words(self):
        """Checks for words that often occur in conjunction with the
        user's primary query, but are deemed undesirable.
        """
        self.bycatch_word_overlap = self._overlap(self.bycatch_words)
        return self.bycatch_word_overlap

    def get_research_words(self):
        """Checks for words that correspond to specific experimental designs."""
        self.research_words = [
            "big data",
            "data",
            "analytics",
            "randomized controlled trial",
            "RCT",
            "moderation",
            "community",
            "social media",
            "conversational",
            "control",
            "randomized",
            "systemic",
            "analysis",
            "thematic",
            "review",
            "study",
            "case series",
            "case report",
            "double blind",
            "ecological",
            "survey",
        ]
        self.research_word_overlap = self._overlap(self.research_words)
        return self.research_word_overlap

    def get_wordscore(self) -> int:
        """Returns a score, which is the number of target words minus the number of undesirable words.
        A positive score suggests that the paper is more likely than not to be a match.
        A negative score suggests that the paper is likely to be unrelated to the user's primary query."""
        target_intersection = compute_intersection(TARGET_WORDS, self.all_words)
        bycatch_intersection = compute_intersection(BYCATCH_WORDS, self.all_words)
        return len(target_intersection) - len(bycatch_intersection)

    def get_doi(self) -> str:
        """Approximates a possible DOI, assuming the file is saved in YYMMDD_DOI.pdf format."""
        self.getting_doi = path.basename(self.search_text)
        self.doi = self.getting_doi[7:-4]
        self.doi = self.doi[:7] + "/" + self.doi[7:]
        return self.doi

    def get_data_entry(self) -> dict:
        """Returns a dictionary entry. Ideally, this will someday work through a DataEntry class."""
        self.data = {
            "DOI": self.get_doi(),
            "wordscore": self.get_wordscore(),
            "frequency": FreqDist(self.all_words).most_common(5),
            "study_design": FreqDist(self.research_word_overlap).most_common(3),
        }

        return self.data
