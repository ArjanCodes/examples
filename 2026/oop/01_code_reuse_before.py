class DatabaseService:
    def fetch_paid_order_totals(self) -> list[int]:
        return [120, 75, 210]


class Logger:
    def log(self, message: str) -> None:
        print(f"[logger] {message}")


class DailySalesReport(DatabaseService, Logger):
    def generate(self) -> None:
        totals = self.fetch_paid_order_totals()
        self.log(f"Daily sales: {sum(totals)} EUR")


def main() -> None:
    DailySalesReport().generate()


if __name__ == "__main__":
    main()
