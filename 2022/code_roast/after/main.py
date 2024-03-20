import time

from scrape.config import read_config
from scrape.export import export_data
from scrape.fetch import fetch_terms_from_pdf_files
from scrape.log import log_msg


def main() -> None:
    # read the configuration settings from a JSON file
    config = read_config("./config.json")

    # fetch data from pdf files and export it
    start = time.perf_counter()
    result = fetch_terms_from_pdf_files(config)
    export_data(result, config.export_dir)
    elapsed = time.perf_counter() - start
    log_msg(f"\n[sciscraper]: Extraction finished in {elapsed} seconds.\n")


if __name__ == "__main__":
    main()
