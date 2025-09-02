from singleton import Singleton


class ModelLoader(metaclass=Singleton):
    def __init__(self):
        print("Loading large model...")

    def predict(self, data: str) -> str:
        return f"Prediction for {data}"


def predict(data: str) -> str:
    model = ModelLoader()
    return model.predict(data)


def main() -> None:
    predictions = [predict(f"data_{i}") for i in range(5)]
    for pred in predictions:
        print(pred)


if __name__ == "__main__":
    main()
