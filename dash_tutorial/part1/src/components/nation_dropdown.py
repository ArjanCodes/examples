from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from . import ids


def render(app: Dash) -> html.Div:
    all_nations = ["South Korea", "China", "Canada"]

    @app.callback(
        Output(ids.NATION_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_NATIONS_BUTTON, "n_clicks"),
    )
    def select_all_nations(_: int) -> list[str]:
        return all_nations

    return html.Div(
        children=[
            html.H6("Nation"),
            dcc.Dropdown(
                id=ids.NATION_DROPDOWN,
                options=[{"label": year, "value": year} for year in all_nations],
                value=all_nations,
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children=["Select All"],
                id=ids.SELECT_ALL_NATIONS_BUTTON,
                n_clicks=0,
            ),
        ]
    )
