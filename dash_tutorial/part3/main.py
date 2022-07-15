import i18n
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from src.components.layout import create_layout
from src.data.loader import load_transaction_data
from src.data.source import DataSource

LOCALE = "nl"
DATA_PATH = "./data/transactions.csv"


def main() -> None:

    # set the locale and load the translations
    i18n.set("locale", LOCALE)
    i18n.load_path.append("locale")

    # load the data and create the data manager
    data = load_transaction_data(DATA_PATH, LOCALE)
    data = DataSource(data)

    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = i18n.t("general.app_title")
    app.layout = create_layout(app, data)
    app.run()


if __name__ == "__main__":
    main()
