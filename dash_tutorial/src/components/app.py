from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP


def create_app(title: str) -> Dash:
    app = Dash(
        __name__,
        external_stylesheets=[
            BOOTSTRAP,
            "https://codepen.io/chriddyp/pen/bWLwgP.css",
        ],
    )
    app.title = title
    return app
