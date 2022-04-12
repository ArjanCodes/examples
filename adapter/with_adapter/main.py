import json

from bs4 import BeautifulSoup

from bs_adapter import BeautifulSoupJSONAdapter
from experiment import Experiment


def main() -> None:
    with open("config.xml", "r", encoding="utf8") as file:
        config_xml = file.read()
    bs_xml = BeautifulSoup(config_xml, "xml")

    with open("config.json", encoding="utf8") as file:
        config_json = json.load(file)
    bs_json = BeautifulSoupJSONAdapter(config_json)
    experiment = Experiment(bs_json)
    experiment.run()


if __name__ == "__main__":
    main()
