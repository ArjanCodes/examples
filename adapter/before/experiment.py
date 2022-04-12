from bs4 import BeautifulSoup


class Experiment:
    def __init__(self, config: BeautifulSoup) -> None:
        self.config = config

    def load_data(self) -> None:
        data_path = self.config.find("data_path")
        if data_path:
            print(f"Loading data from {data_path.get_text()}.")
        else:
            raise ValueError("No data path specified.")

    def setup_log(self) -> None:
        log_path = self.config.find("log_path")
        if log_path:
            print(f"Logging to {log_path.get_text()}.")
        else:
            raise ValueError("No log path specified.")

    def train_model(self) -> None:
        epoch_count = self.config.find("epoch_count")
        if epoch_count:
            print(f"Training for {epoch_count.get_text()} epochs.")
        else:
            raise ValueError("No epoch count specified.")

    def run(self) -> None:
        self.load_data()
        self.setup_log()
        self.train_model()
