import i18n
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from src.components.layout import create_layout
from src.data import load_transaction_data

LOCALE = "nl"
DEBUG = False
DATA_PATH = "./data/transactions.csv"


def main() -> None:

    # load the data
    data = load_transaction_data(DATA_PATH, LOCALE)

    # set the locale and load the translations
    i18n.set("locale", LOCALE)
    i18n.load_path.append("locale")

    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = i18n.t("general.app_title")
    app.layout = create_layout(app, data)
    app.run_server(debug=DEBUG)


if __name__ == "__main__":
    main()
