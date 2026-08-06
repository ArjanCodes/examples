from typing import Protocol


class OrderDatabase(Protocol):
    def fetch_paid_order_totals(self) -> list[int]: ...


class Logger(Protocol):
    def log(self, message: str) -> None: ...


class InMemoryOrderDatabase:
    def fetch_paid_order_totals(self) -> list[int]:
        return [120, 75, 210]


class ConsoleLogger:
    def log(self, message: str) -> None:
        print(f"[report] {message}")


class DailySalesReport:
    def __init__(self, database: OrderDatabase, logger: Logger) -> None:
        self.database = database
        self.logger = logger

    def generate(self) -> None:
        totals = self.database.fetch_paid_order_totals()
        self.logger.log(f"Daily sales: {sum(totals)} EUR")


def main() -> None:
    report = DailySalesReport(InMemoryOrderDatabase(), ConsoleLogger())
    report.generate()


if __name__ == "__main__":
    main()
