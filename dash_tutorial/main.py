from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from src.config import load_settings
from src.layout import create_layout


def create_app(title: str) -> Dash:
    app = Dash(
        external_stylesheets=[BOOTSTRAP],
    )
    app.title = title
    return app


def main() -> None:
    settings = load_settings()
    app = create_app(settings.app.title)
    create_layout(app, settings)
    app.run_server(debug=settings.debug)


if __name__ == "__main__":
    main()
