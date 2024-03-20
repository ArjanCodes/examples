from fnmatch import fnmatch
from os import listdir, path

import pandas as pd
from tqdm import tqdm

from scrape.config import ScrapeConfig
from scrape.pdf import PDFScraper
from scrape.scraper import Scraper


def fetch_terms_from_doi(target: str, scraper: Scraper) -> pd.DataFrame:
    print(f"\n[sciscraper]: Getting entries from file: {target}")
    with open(target, newline="") as f:
        df = [doi for doi in pd.read_csv(f, usecols=["DOI"])["DOI"]]
        search_terms = [search_text for search_text in df if search_text is not None]
        return pd.DataFrame(
            [scraper.scrape(search_text) for search_text in tqdm(search_terms)]
        )


def fetch_terms_from_pubid(target: pd.DataFrame, scraper: Scraper) -> pd.DataFrame:
    df = target.explode("cited_dimensions_ids", "title")
    search_terms = (
        search_text
        for search_text in df["cited_dimensions_ids"]
        if search_text is not None
    )
    src_title = pd.Series(df["title"])

    return pd.DataFrame(
        [scraper.scrape(search_text) for search_text in tqdm(list(search_terms))]
    ).join(src_title)


def fetch_terms_from_pdf_files(config: ScrapeConfig) -> pd.DataFrame:
    search_terms = [
        path.join(config.paper_folder, file)
        for file in listdir(config.paper_folder)
        if fnmatch(path.basename(file), "*.pdf")
    ]
    scraper = PDFScraper(
        config.research_words, config.bycatch_words, config.target_words
    )
    return pd.DataFrame([scraper.scrape(file) for file in tqdm(search_terms)])
