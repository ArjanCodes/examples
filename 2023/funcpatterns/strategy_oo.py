from abc import ABC, abstractmethod


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list[int]) -> list[int]:
        pass


class BubbleSortStrategy(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        data = data.copy()
        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
        return data


class QuickSortStrategy(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        data = data.copy()
        if len(data) <= 1:
            return data
        else:
            pivot = data.pop()
            greater: list[int] = []
            lesser: list[int] = []
            for item in data:
                if item > pivot:
                    greater.append(item)
                else:
                    lesser.append(item)
            return self.sort(lesser) + [pivot] + self.sort(greater)


class Context:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy

    def sort(self, data: list[int]) -> list[int]:
        return self._strategy.sort(data)


def main() -> None:
    context = Context(BubbleSortStrategy())
    print(context.sort([1, 5, 3, 4, 2]))  # Using Bubble Sort

    context.set_strategy(QuickSortStrategy())
    print(context.sort([1, 5, 3, 4, 2]))  # Using Quick Sort


if __name__ == "__main__":
    main()
