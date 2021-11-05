import logging
from datetime import datetime

now = datetime.now()
date = now.strftime("%y%m%d")

logging.basicConfig(
    filename=f"{date}_scraper.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)


def log_msg(msg: str) -> None:
    logging.info(msg)
    print(msg)
