from typing import Any, Callable

ConfigGetter = Callable[[str], Any]


class Experiment:
    def __init__(self, config_getter: ConfigGetter) -> None:
        self.config_getter = config_getter

    def load_data(self) -> None:
        data_path = self.config_getter("data_path")
        if data_path:
            print(f"Loading data from {data_path}.")
        else:
            raise ValueError("No data path specified.")

    def setup_log(self) -> None:
        log_path = self.config_getter("log_path")
        if log_path:
            print(f"Logging to {log_path}.")
        else:
            raise ValueError("No log path specified.")

    def train_model(self) -> None:
        epoch_count = self.config_getter("epoch_count")
        if epoch_count:
            print(f"Training for {epoch_count} epochs.")
        else:
            raise ValueError("No epoch count specified.")

    def run(self) -> None:
        self.load_data()
        self.setup_log()
        self.train_model()
