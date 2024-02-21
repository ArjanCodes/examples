class WeightLimitExceededError(Exception):
    """Raised when the weight limit of a container is exceeded."""

    def __init__(self, limit: int, current: int):
        super().__init__(f"Weight limit exceeded: limit= {limit}, current= {current}")
        self.limit = limit
        self.current = current


class WeightNegativeError(Exception):
    """Raised when the weight of an item is negative."""

    def __init__(self, weight: int):
        self.weight = weight
        self.message = f"Weight cannot be negative: weight= {weight}"


class Container:
    def __init__(self, limit: int):
        self.limit = limit
        self.current_weight = 0

    def load_item(self, weight: int):
        if weight < 0:
            raise WeightNegativeError(weight)

        new_weight = self.current_weight + weight

        if new_weight > self.limit:
            raise WeightLimitExceededError(self.limit, new_weight)

        self.current_weight = new_weight
        print("Item loaded")


def main() -> None:
    try:
        container = Container(limit=100)
        container.load_item(50)  # This should work fine
        container.load_item(-60)  # This will raise a WeightLimitExceededError
    except WeightLimitExceededError as e:
        print(e)
    except WeightNegativeError as e:
        print(e.message)


if __name__ == "__main__":
    main()
