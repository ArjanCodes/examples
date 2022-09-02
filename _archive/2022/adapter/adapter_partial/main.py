import json
from functools import partial

from bs4 import BeautifulSoup

from experiment import Experiment
from xml_adapter import get_from_bs


def main() -> None:

    with open("config.json", encoding="utf8") as file:
        config = json.load(file)
    with open("config.xml", encoding="utf8") as file:
        config_xml = file.read()
    soup = BeautifulSoup(config_xml, "xml")
    bs_adapter_fn = partial(get_from_bs, soup)
    experiment = Experiment(config.get)
    # experiment = Experiment(bs_adapter_fn)
    experiment.run()


if __name__ == "__main__":
    main()
