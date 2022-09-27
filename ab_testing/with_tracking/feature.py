import os
from dataclasses import dataclass

import requests
from growthbook import GrowthBook


@dataclass
class Config:
    show_save_button: bool = True


def read_config() -> Config:

    api_key = os.getenv("GROWTHBOOK_KEY") or ""
    response = requests.get(
        f"https://cdn.growthbook.io/api/features/{api_key}", timeout=5
    )
    features = response.json()["features"]
    growth_book = GrowthBook(
        features=features,
    )

    return Config(show_save_button=growth_book.isOn("show_save_button"))
