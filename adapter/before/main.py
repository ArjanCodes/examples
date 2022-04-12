from bs4 import BeautifulSoup

from experiment import Experiment


def main() -> None:
    with open("config.xml", "r", encoding="utf8") as file:
        config = file.read()
    bs_xml = BeautifulSoup(config, "xml")
    experiment = Experiment(bs_xml)
    experiment.run()


if __name__ == "__main__":
    main()
