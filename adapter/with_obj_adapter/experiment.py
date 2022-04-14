from config_protocol import Config


class Experiment:
    def __init__(self, config: Config) -> None:
        self.config = config

    def load_data(self) -> None:
        data_path = self.config.get("data_path")
        if data_path:
            print(f"Loading data from {data_path}.")
        else:
            raise ValueError("No data path specified.")

    def setup_log(self) -> None:
        log_path = self.config.get("log_path")
        if log_path:
            print(f"Logging to {log_path}.")
        else:
            raise ValueError("No log path specified.")

    def train_model(self) -> None:
        epoch_count = self.config.get("epoch_count")
        if epoch_count:
            print(f"Training for {epoch_count} epochs.")
        else:
            raise ValueError("No epoch count specified.")

    def run(self) -> None:
        self.load_data()
        self.setup_log()
        self.train_model()
