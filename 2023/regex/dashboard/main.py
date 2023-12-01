from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from src.components.layout import create_layout
from src.data.reader import load_json


def main() -> None:
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "Regex dashboard"
    app.layout = create_layout(app)
    app.run()


if __name__ == "__main__":
    main()