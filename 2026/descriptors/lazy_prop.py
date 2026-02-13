from typing import Any, Callable, Self


class lazy_property[T]:
    def __init__(self, func: Callable[[Any], T]) -> None:
        self.func = func
        self.name = func.__name__
        self.storage_name = f"_{self.name}"

    def __get__(self, instance: Any | None, owner: type) -> T | Self:
        if instance is None:
            return self
        if hasattr(instance, self.storage_name):
            return getattr(instance, self.storage_name)
        value = self.func(instance)
        setattr(instance, self.storage_name, value)
        return value


class Report:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self.rows = rows

    @lazy_property
    def revenue_by_country(self) -> dict[str, float]:
        print("computing revenue_by_country...")
        result: dict[str, float] = {}
        for r in self.rows:
            country = str(r["country"])
            revenue = float(r["revenue"])
            result[country] = result.get(country, 0.0) + revenue
        return result


def main() -> None:
    rows: list[dict[str, Any]] = [
        {"country": "NL", "revenue": 10},
        {"country": "NL", "revenue": 5},
    ]

    rep = Report(rows)
    print(rep.revenue_by_country)
    print(rep.revenue_by_country)  # cached


if __name__ == "__main__":
    main()
