from bs4 import BeautifulSoup

from experiment import Experiment
from xml_adapter import XMLAdapter


def main() -> None:
    with open("config.xml", encoding="utf8") as file:
        config_xml = file.read()
    bs_xml = BeautifulSoup(config_xml, "xml")
    adapter = XMLAdapter(bs_xml)
    experiment = Experiment(adapter)
    experiment.run()


if __name__ == "__main__":
    main()
