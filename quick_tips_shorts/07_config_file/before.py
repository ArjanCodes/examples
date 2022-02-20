# Machine learning parameters
EPOCH_COUNT = 40
LR = 5e-5
BATCH_SIZE = 64
LOG_PATH = "./runs"
DATA_PATH = "./raw_data"


def load_data(path: str):
    print(f"Loading data from {path}...")


def setup_logging(path: str):
    print(f"Setting up logging to {path}...")


def train_model(epochs: int, learning_rate: float, batch_size: int):
    print(
        f"Training model for {epochs} epochs, LR {learning_rate}, batch size {batch_size}..."
    )


def main():
    load_data(DATA_PATH)
    setup_logging(LOG_PATH)
    train_model(EPOCH_COUNT, LR, BATCH_SIZE)


if __name__ == "__main__":
    main()
