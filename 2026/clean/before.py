import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Protocol

# ---------- Domain-ish types ----------


@dataclass(frozen=True)
class Row:
    data: dict[str, Any]


@dataclass(frozen=True)
class SalesSummary:
    total_orders: int
    total_revenue: float


# ---------- Abstraction (nice!) ----------


class ReportService(Protocol):
    """Clean interface. The chaos is hidden in the implementation + wiring."""

    def run(self, source: str, target: str) -> None: ...


# ---------- Implementation (not nice) ----------


class DefaultReportService:
    """
    The call site looks clean: service.run(source, target)

    But the actual "API" is this constructor: a bag of settings and flags.
    """

    def __init__(
        self,
        *,
        delimiter: str,
        encoding: str,
        expected_fields: tuple[str, ...],
        allow_negative_revenue: bool,
        drop_invalid_rows: bool,
        country: str | None,
        min_revenue: float,
        revenue_field: str,
        order_id_field: str,
        report_title: str,
        currency_symbol: str,
        include_debug_footer: bool,
        row_transform: Callable[[Row], Row] | None,
        on_error: Callable[[Exception, Row | None], None] | None,
    ) -> None:
        self._delimiter = delimiter
        self._encoding = encoding
        self._expected_fields = expected_fields
        self._allow_negative_revenue = allow_negative_revenue
        self._drop_invalid_rows = drop_invalid_rows
        self._country = country
        self._min_revenue = min_revenue
        self._revenue_field = revenue_field
        self._order_id_field = order_id_field
        self._report_title = report_title
        self._currency_symbol = currency_symbol
        self._include_debug_footer = include_debug_footer
        self._row_transform = row_transform
        self._on_error = on_error

    def run(self, source: str, target: str) -> None:
        path = Path(source)

        # --- Load + parse CSV (for real this time) ---
        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {path.resolve()}")

        raw_rows: list[Row] = []
        with path.open("r", newline="", encoding=self._encoding) as f:
            reader = csv.DictReader(f, delimiter=self._delimiter)
            # DictReader already uses the header row as keys.
            for d in reader:
                # Keep raw strings; validation will decide what to do.
                raw_rows.append(Row(data=dict(d)))

        # --- Validate + Transform + Filter ---
        processed: list[Row] = []
        for row in raw_rows:
            try:
                # Required fields must exist AND be non-empty
                missing_or_empty = [
                    f for f in self._expected_fields if not row.data.get(f)
                ]
                if missing_or_empty:
                    raise ValueError(f"Missing/empty fields: {missing_or_empty}")

                # Coerce revenue
                revenue_raw = row.data[self._revenue_field]
                revenue = float(revenue_raw)

                if revenue < 0 and not self._allow_negative_revenue:
                    raise ValueError("Negative revenue is not allowed")

                # Optional transform hook
                if self._row_transform is not None:
                    row = self._row_transform(row)

                # Filters
                if (
                    self._country is not None
                    and row.data.get("country") != self._country
                ):
                    continue
                if revenue < self._min_revenue:
                    continue

                processed.append(row)

            except Exception as exc:
                if self._on_error is not None:
                    self._on_error(exc, row)

                if self._drop_invalid_rows:
                    continue
                raise

        # --- Aggregate ---
        total_orders = 0
        total_revenue = 0.0
        for row in processed:
            total_orders += 1
            total_revenue += float(row.data[self._revenue_field])

        summary = SalesSummary(total_orders=total_orders, total_revenue=total_revenue)

        # --- Export ---
        # target is still mostly decorative, but we pretend it's a real output concern.
        if target == "stdout":
            print(self._report_title)
            print(f"Orders: {summary.total_orders}")
            print(f"Revenue: {self._currency_symbol}{summary.total_revenue:.2f}")
        else:
            out = Path(target)
            out.write_text(
                "\n".join(
                    [
                        self._report_title,
                        f"Orders: {summary.total_orders}",
                        f"Revenue: {self._currency_symbol}{summary.total_revenue:.2f}",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            print(f"Wrote report to {out.resolve()}")

        if self._include_debug_footer:
            print("--- DEBUG ---")
            print(
                f"source={source!r} target={target!r} "
                f"delimiter={self._delimiter!r} encoding={self._encoding!r}"
            )
            print(
                f"filters: country={self._country!r}, min_revenue={self._min_revenue}"
            )
            print(
                f"fields: revenue_field={self._revenue_field!r}, order_id_field={self._order_id_field!r}"
            )
            print(f"loaded_rows={len(raw_rows)} processed_rows={len(processed)}")


# ---------- "DI container" wiring ----------


class Container:
    def __init__(self) -> None:
        self._settings = self._load_settings()

    def _load_settings(self) -> dict[str, Any]:
        # Pretend this comes from env vars, YAML, or a config framework.
        return {
            "delimiter": ",",
            "encoding": "utf-8",
            "expected_fields": ("order_id", "country", "revenue"),
            "allow_negative_revenue": False,
            "drop_invalid_rows": True,
            "country": "NL",
            "min_revenue": 10.0,
            "revenue_field": "revenue",
            "order_id_field": "order_id",
            "report_title": "Sales Report (NL, revenue >= 10)",
            "currency_symbol": "€",
            "include_debug_footer": True,
        }

    def report_service(self) -> ReportService:
        def on_error(exc: Exception, row: Row | None) -> None:
            # Cross-cutting concern living in the container, naturally.
            # Also: the best place to hide production bugs.
            payload = row.data if row else None
            print(f"[warn] {exc} row={payload}")

        return DefaultReportService(
            delimiter=str(self._settings["delimiter"]),
            encoding=str(self._settings["encoding"]),
            expected_fields=tuple(self._settings["expected_fields"]),
            allow_negative_revenue=bool(self._settings["allow_negative_revenue"]),
            drop_invalid_rows=bool(self._settings["drop_invalid_rows"]),
            country=self._settings["country"],
            min_revenue=float(self._settings["min_revenue"]),
            revenue_field=str(self._settings["revenue_field"]),
            order_id_field=str(self._settings["order_id_field"]),
            report_title=str(self._settings["report_title"]),
            currency_symbol=str(self._settings["currency_symbol"]),
            include_debug_footer=bool(self._settings["include_debug_footer"]),
            row_transform=None,
            on_error=on_error,
        )


# ---------- Call site (super clean!) ----------


def main() -> None:
    container = Container()
    service = container.report_service()
    service.run(source="sales.csv", target="stdout")


if __name__ == "__main__":
    main()
