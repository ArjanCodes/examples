from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from src.callbacks import register_callbacks
from src.components.app import create_app
from src.config import SETTINGS
from src.layout import create_layout


def create_app_old(title: str) -> Dash:
    app = Dash(
        external_stylesheets=[BOOTSTRAP],
    )
    app.title = title
    return app


def main() -> None:
    print(__name__)
    app = create_app_old(SETTINGS.app.title)
    app.layout = create_layout()
    register_callbacks(app)
    app.run_server(debug=SETTINGS.debug)


if __name__ == "__main__":
    main()
