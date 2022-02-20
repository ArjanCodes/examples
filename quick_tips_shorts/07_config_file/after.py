import json


def load_data(path: str):
    print(f"Loading data from {path}...")


def setup_logging(path: str):
    print(f"Setting up logging to {path}...")


def train_model(epochs: int, learning_rate: float, batch_size: int):
    print(
        f"Training model for {epochs} epochs, LR {learning_rate}, batch size {batch_size}..."
    )


def main():
    data = json.load(open(file="./config.json", encoding="utf-8"))
    load_data(data["data_path"])
    setup_logging(data["log_path"])
    train_model(data["epoch_count"], data["lr"], data["batch_size"])


if __name__ == "__main__":
    main()
