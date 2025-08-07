class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            print(f"Creating instance of {cls.__name__}")
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


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