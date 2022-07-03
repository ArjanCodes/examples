import i18n
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from src.components.layout import create_layout
from src.config import load_settings
from src.data import load_transaction_data


def main() -> None:
    settings = load_settings()

    # load the data
    data = load_transaction_data(settings.data_path)

    # set the locale and load the translations
    i18n.load_path.append("locale")

    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = i18n.t("general.app_title")
    app.layout = create_layout(app, data)
    app.run_server(debug=settings.debug)


if __name__ == "__main__":
    main()
