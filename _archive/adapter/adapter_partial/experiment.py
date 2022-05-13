from typing import Any, Callable

ConfigGetter = Callable[[str], Any]


class Experiment:
    def __init__(self, config_getter: ConfigGetter) -> None:
        self.config_getter = config_getter

    def load_data(self) -> None:
        data_path = self.config_getter("data_path")
        if not data_path:
            raise ValueError("No data path specified.")
        print(f"Loading data from {data_path}.")

    def setup_log(self) -> None:
        log_path = self.config_getter("log_path")
        if not log_path:
            raise ValueError("No log path specified.")
        print(f"Logging to {log_path}.")

    def train_model(self) -> None:
        epoch_count = self.config_getter("epoch_count")
        if not epoch_count:
            raise ValueError("No epoch count specified.")
        print(f"Training for {epoch_count} epochs.")

    def run(self) -> None:
        self.load_data()
        self.setup_log()
        self.train_model()
