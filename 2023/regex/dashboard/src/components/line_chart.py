import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

from . import ids


def render(app: Dash, data_frame: pd.DataFrame) -> html.Div:
    app.callback(Output(ids.LINE_CHART, "figure"), Input("dropdown-selection", "value"))
    fig = px.line(data_frame=data_frame).update_layout(
        xaxis_title="Length of string",
        yaxis_title="Time elapsed",
        legend_title="Patterns",
    )
    return html.Div(dcc.Graph(figure=fig), id=ids.LINE_CHART)
