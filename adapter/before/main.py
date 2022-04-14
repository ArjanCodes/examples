import json

from experiment import Experiment


def main() -> None:
    with open("config.json", encoding="utf8") as file:
        config = json.load(file)
    experiment = Experiment(config)
    experiment.run()


if __name__ == "__main__":
    main()
