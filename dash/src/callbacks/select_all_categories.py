import dash
import src
from dash.dependencies import Input, Output

SETTINGS = src.config.load_settings()


def register(app: dash.Dash) -> None:
    @app.callback(
        Output(SETTINGS.components.category_dropdown.id, "value"),
        [
            Input(SETTINGS.components.year_dropdown.id, "value"),
            Input(SETTINGS.components.month_dropdown.id, "value"),
            Input(SETTINGS.components.category_button.id, "n_clicks"),
        ],
    )
    def _select_all_categories(year: list[int], month: list[int], _: list[int]) -> list[str]:
        categories: list[str] = list(
            src.transactions.load_transaction_data()
            .query(
                f"({src.schema.YearColumnSchema.year} == {year}) "
                f"& ({src.schema.MonthColumnSchema.month} == {month})"
            )
            .loc[:, src.schema.RawTransactionsSchema.category]
            .unique()
        )
        return sorted(categories)
