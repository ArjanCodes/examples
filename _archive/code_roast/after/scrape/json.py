import json
import time
from json.decoder import JSONDecodeError
from typing import Optional

## Scraping Related Imports
import requests
from requests.exceptions import HTTPError, RequestException

from scrape.log import log_msg


class JSONScraper:
    """The JSONScrape class takes the provided string from a prior list comprehension.
    Using that string value, it gets the resulting JSON data, parses it, and then returns a dictionary, which gets appended to a list.
    """

    def __init__(self, dimensions_url: str) -> None:
        self.dimensions_url = dimensions_url

    def download(self, search_text: str) -> dict:
        """The download method generates a session and a querystring that gets sent to the website. This returns a JSON entry.
        The JSON entry is loaded and specific values are identified for passing along, back to a dataframe.
        """
        self.sessions = requests.Session()
        self.search_field = self.specify_search(search_text)
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
            r = self.sessions.get(self.dimensions_url, params=querystring)
            r.raise_for_status()
            log_msg(str(r.status_code))
            self.docs = json.loads(r.text)["docs"]

        except (JSONDecodeError, RequestException) as e:
            print(
                f"\n[sciscraper]: An error occurred while searching for {search_text}.\
                \n[sciscraper]: Proceeding to next item in sequence.\
                Cause of error: {e}\n"
            )
            pass

        except HTTPError as f:
            print(
                f"\n[sciscraper]: Access to {self.dimensions_url} denied while searching for {search_text}.\
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
