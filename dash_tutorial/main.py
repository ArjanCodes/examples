from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from src.config import load_settings
from src.layout import create_layout


def main() -> None:
    settings = load_settings()
    app = Dash(
        external_stylesheets=[BOOTSTRAP],
    )
    app.title = settings.app.title
    app.layout = create_layout(settings)
    app.run_server(debug=settings.debug)


if __name__ == "__main__":
    main()
