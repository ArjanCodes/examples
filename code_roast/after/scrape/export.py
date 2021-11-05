import random
from datetime import datetime
from typing import Optional

import pandas as pd

from scrape.dir import change_dir
from scrape.log import log_msg


def export_data(dataframe: Optional[pd.DataFrame], export_dir: str):
    now = datetime.now()
    date = now.strftime("%y%m%d")
    with change_dir(export_dir):
        print_id = random.randint(0, 100)
        export_name = f"{date}_DIMScrape_Refactor_{print_id}.csv"
        dataframe.to_csv(export_name)
        print(dataframe.head())
        log_msg(
            f"\n[sciscraper]: A spreadsheet was exported as {export_name} in {export_dir}.\n"
        )
