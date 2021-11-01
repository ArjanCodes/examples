import __future__

from pdf_scrape import PDFScrape

__version__ = "1.01"
__author__ = "John Fallot"

import datetime
import json
import logging
import os
import random
import re
import time
from contextlib import contextmanager, suppress
from fnmatch import fnmatch
from json.decoder import JSONDecodeError
from os import PathLike, listdir, path
from os.path import isdir
from typing import Optional

import nltk
import pandas as pd

## Language Processing Related Imports
import pdfplumber

## Scraping Related Imports
import requests
from bs4 import BeautifulSoup
from nltk import FreqDist
from nltk.corpus import names, stopwords
from nltk.tokenize import word_tokenize
from requests.exceptions import HTTPError, RequestException
from tqdm import tqdm

# nltk.download("stopwords")
# nltk.download("names")
# nltk.download("punkt")

# ==============================================
#    CONFIGS
# ==============================================

now = datetime.datetime.now()
date = now.strftime("%y%m%d")
export_dir = os.path.realpath("PDN Scraper Exports")
msg_error_1 = "[sciscraper]: HTTP Error Encountered, moving to next available object. Reason Given:"

logging.basicConfig(
    filename=f"{date}_scraper.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)

PRIME_SRC = os.path.realpath("211001_PDN_studies_9.csv")
URL_DMNSNS = "https://app.dimensions.ai/discover/publication/results.json"
RESEARCH_DIR = os.path.realpath(f"{date}_PDN Research Papers From Scrape")
URL_SCIHUB = "https://sci-hubtw.hkvisa.net/"

# ==============================================
#    SCRAPE RELATED CLASSES & SUBCLASSES
# ==============================================


class ScrapeRequest:
    """The abstraction of the program's web scraping requests, which dynamically returns its appropriate subclasses based on the provided inputs."""

    _registry = {}

    def __init_subclass__(cls, slookup_code, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry[slookup_code] = cls

    def __new__(cls, s_bool: bool):
        """The ScrapeRequest class looks for the boolean value passed to it from the FileRequest class.
        A value of True, or 1, would return a SciHubScrape subclass.
        Whereas a value of False, of 0, would return a JSONScrape subclass.
        """
        if not isinstance(s_bool, bool):
            raise TypeError
        if s_bool:
            slookup_code = "sci"
        else:
            slookup_code = "json"

        subclass = cls._registry[slookup_code]

        obj = object.__new__(subclass)
        return obj

    def download(self) -> None:
        raise NotImplementedError


class SciHubScrape(ScrapeRequest, slookup_code="sci"):
    """The SciHubScrape class takes the provided string from a prior list comprehension.
    Using that string value, it posts it to the selected website.
    Then, it downloads the ensuing pdf file that appears as a result of that query.
    """

    def download(self, search_text: str):
        """The download method generates a session and a payload that gets posted as a search query to the website.
        This search should return a pdf.
        Once the search is found, it is parsed with BeautifulSoup.
        Then, the link to download that pdf is isolated.
        """
        self.sessions = requests.Session()
        self.base_url = URL_SCIHUB
        print(
            f"[sciscraper]: Delving too greedily and too deep for download links for {search_text}, by means of dark and arcane magicx.",
            end="\r",
        )
        self.payload = {"request": f"{search_text}"}
        with change_dir(RESEARCH_DIR):
            time.sleep(1)
            with suppress(
                requests.exceptions.HTTPError, requests.exceptions.RequestException
            ):
                r = self.sessions.post(url=self.base_url, data=self.payload)
                r.raise_for_status()
                logging.info(r.status_code)
                soup = BeautifulSoup(r.text, "lxml")
                self.links = list(
                    ((item["onclick"]).split("=")[1]).strip("'")
                    for item in soup.select("button[onclick^='location.href=']")
                )
                self.enrich_scrape()

    def enrich_scrape(self, search_text: str):
        """With the link to download isolated, it is followed and thereby downloaded.
        It is sent as bytes to a temporary text file, as a middleman of sorts.
        The temporary text file is then used as a basis to generate a new pdf.
        The temporary text file is then deleted in preparation for the next pdf.
        """
        for link in self.links:
            paper_url = f"{link}=true"
            paper_title = f'{date}_{search_text.replace("/","")}.pdf'
            time.sleep(1)
            paper_content = (
                requests.get(paper_url, stream=True, allow_redirects=True)
            ).content
            with open("temp_file.txt", "wb") as _tempfile:
                _tempfile.write(paper_content)
            with open(paper_title, "wb") as file:
                for line in open("temp_file.txt", "rb").readlines():
                    file.write(line)
            os.remove("temp_file.txt")


class JSONScrape(ScrapeRequest, slookup_code="json"):
    """The JSONScrape class takes the provided string from a prior list comprehension.
    Using that string value, it gets the resulting JSON data, parses it, and then returns a dictionary, which gets appended to a list.
    """

    def download(self, search_text: str) -> dict:
        """The download method generates a session and a querystring that gets sent to the website. This returns a JSON entry.
        The JSON entry is loaded and specific values are identified for passing along, back to a dataframe.
        """
        self.sessions = requests.Session()
        self.search_field = self.specify_search(search_text)
        self.base_url = URL_DMNSNS
        print(
            f"[sciscraper]: Searching for {search_text} via a {self.search_field}-style search.",
            end="\r",
        )
        querystring = {
            "search_mode": "content",
            "search_text": f"{search_text}",
            "search_type": "kws",
            "search_field": f"{self.search_field}",
        }
        time.sleep(1)

        try:
            r = self.sessions.get(self.base_url, params=querystring)
            r.raise_for_status()
            logging.info(r.status_code)
            self.docs = json.loads(r.text)["docs"]

        except (JSONDecodeError, RequestException) as e:
            print(
                f"\n[sciscraper]: An error occurred while searching for {search_text}.\
                \n\[sciscraper]: Proceeding to next item in sequence.\
                Cause of error: {e}\n"
            )
            pass

        except HTTPError as f:
            print(
                f"\n[sciscraper]: Access to {self.base_url} denied while searching for {search_text}.\
                \n[sciscraper]: Terminating sequence. Cause of error: {f}\
                \n"
            )
            quit()

        for item in self.docs:
            self.data = self.get_data_entry(
                item,
                keys=[
                    "title",
                    "author_list",
                    "publisher",
                    "pub_date",
                    "doi",
                    "id",
                    "abstract",
                    "acknowledgements",
                    "journal_title",
                    "volume",
                    "issue",
                    "times_cited",
                    "mesh_terms",
                    "cited_dimensions_ids",
                ],
            )
        return self.data

    def specify_search(self, search_text: str) -> str:
        """Determines whether the dimensions.ai query will be for a full_search or just for the doi."""
        if search_text.startswith("pub"):
            self.search_field = "full_search"
        else:
            self.search_field = "doi"
        return self.search_field

    def get_data_entry(self, item, keys: Optional[list]) -> dict:
        """Based on a provided list of keys and items in the JSON data,
        generates a dictionary entry.
        """
        return {_key: item.get(_key, "") for _key in keys}


# ==============================================
#    CONTEXT MANAGER METACLASS
# ==============================================


@contextmanager
def change_dir(destination: str):
    """Sets a destination for exported files."""
    try:
        __dest = os.path.realpath(destination)
        cwd = os.getcwd()
        if not os.path.exists(__dest):
            os.mkdir(__dest)
        os.chdir(__dest)
        yield
    finally:
        os.chdir(cwd)


# ==============================================
#    FILE REQUEST CLASSES & SUBCLASSES
# ==============================================


class FileRequest:
    """The abstraction of the program's input file classes.
    It dynamically returns its appropriate subclasses based on the provided inputs.
    """

    _registry = {}

    def __init_subclass__(cls, dlookup_code, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry[dlookup_code] = cls

    def __new__(cls, target, slookup_key: bool = None):
        print(target)
        if isdir(target):
            dlookup_code = "fold"
        elif str(target).endswith("csv"):
            dlookup_code = "doi"
        elif isinstance(target, pd.DataFrame):
            dlookup_code = "pub"
        else:
            raise Exception("[sciscraper]: Invalid prefix detected.")

        subclass = cls._registry[dlookup_code]

        obj = object.__new__(subclass)
        obj.target = target
        obj.slookup_key = slookup_key
        obj.scraper = ScrapeRequest(slookup_key)
        return obj

    def fetch_terms(self) -> None:
        raise NotImplementedError


class DOIRequest(FileRequest, dlookup_code="doi"):
    """The DOIRequest class takes a csv and generates a list comprehension.
    The list comprehension is scraped, and then returns a DataFrame.
    """

    def __init__(self, target: str, slookup_key: bool = False):
        self.target = target
        self.slookup_key = slookup_key
        self.scraper = ScrapeRequest(self.slookup_key)

    def fetch_terms(self):
        print(f"\n[sciscraper]: Getting entries from file: {self.target}")
        with open(self.target, newline="") as f:
            self.df = [doi for doi in pd.read_csv(f, usecols=["DOI"])["DOI"]]
            self.search_terms = [
                search_text for search_text in self.df if search_text is not None
            ]
            return pd.DataFrame(
                [
                    self.scraper.download(search_text)
                    for search_text in tqdm(self.search_terms)
                ]
            )


class PubIDRequest(FileRequest, dlookup_code="pub"):
    """The PubIDRequest class takes a DataFrame and generates a list comprehension.
    The list comprehension is scraped, and then returns a DataFrame.
    """

    def __init__(self, target: pd.DataFrame, slookup_key: bool = False):
        if slookup_key:
            print(
                "\n[sciscraper]: Getting Pub IDs from dataframe to download from web..."
            )
        else:
            print(
                "\n[sciscraper]: Expounding upon existing PubIDs to generate a new dataframe..."
            )
        self.target = target
        self.slookup_key = slookup_key
        self.scraper = ScrapeRequest(self.slookup_key)

    def fetch_terms(self):
        self.df = self.target.explode("cited_dimensions_ids", "title")
        self.search_terms = (
            search_text
            for search_text in self.df["cited_dimensions_ids"]
            if search_text is not None
        )
        self.src_title = pd.Series(self.df["title"])

        return pd.DataFrame(
            [
                self.scraper.download(search_text)
                for search_text in tqdm(list(self.search_terms))
            ]
        ).join(self.src_title)


class FolderRequest(FileRequest, dlookup_code="fold"):
    """
    The Folder class takes a directory and generates a list comprehension.
    The list comprehension is scraped, and then returns a DataFrame.
    Unlike other classes, it cannot undergo a SciScrape.
    """

    def __init__(self, target: PathLike[str], slookup_key: bool = False):
        print(f"\n[sciscraper]: Getting files from folder: {target}")
        self.target = target
        if self.slookup_key:
            raise Exception(
                "This action is prohibited. \
                You already have the files that this query would return."
            )
        self.slookup_key = slookup_key
        self.scraper = PDFScrape()

    def fetch_terms(self):
        self.search_terms = [
            path.join(self.target, file)
            for file in listdir(self.target)
            if fnmatch(path.basename(file), "*.pdf")
        ]
        return pd.DataFrame(
            [self.scraper.download(file) for file in tqdm(self.search_terms)]
        )


def fetch_terms_from_folder(folder: str):
    search_terms = [
        path.join(folder, file)
        for file in listdir(folder)
        if fnmatch(path.basename(file), "*.pdf")
    ]
    scraper = PDFScrape()
    return pd.DataFrame([scraper.download(file) for file in tqdm(search_terms)])


# ==============================================
#    EXPORTING, MAIN LOOP, AND MISCELLANY
# ==============================================


def export(dataframe: Optional[pd.DataFrame]):
    with change_dir(export_dir):
        print_id = random.randint(0, 100)
        export_name = f"{date}_DIMScrape_Refactor_{print_id}.csv"
        msg_spreadsheetexported = f"\n[sciscraper]: A spreadsheet was exported as {export_name} in {export_dir}.\n"
        dataframe.to_csv(export_name)
        print(dataframe.head())
        logging.info(msg_spreadsheetexported)
        print(msg_spreadsheetexported)


def main():
    start = time.perf_counter()
    result = fetch_terms_from_folder(folder="papers")
    export(result)
    elapsed = time.perf_counter() - start
    msg_timestamp = f"\n[sciscraper]: Extraction finished in {elapsed} seconds.\n"
    logging.info(msg_timestamp)
    print(msg_timestamp)
    quit()


if __name__ == "__main__":
    main()  # %%
