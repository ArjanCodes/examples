from dash import Dash, html

from . import bar_chart, nation_dropdown


def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className="dropdown-container",
                children=[
                    nation_dropdown.render(app),
                ],
            ),
            bar_chart.render(app),
        ],
    )
