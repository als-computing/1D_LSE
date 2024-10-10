import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dcc, html


def layout():
    """
    Returns the layout for the image viewer.
    """
    return html.Div(
        [
            dbc.Card(
                id="image-card",
                children=[
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dcc.Graph(
                                            id="scatter",
                                            figure=go.Figure(
                                                go.Scattergl(mode="markers"),
                                                layout=go.Layout(
                                                    autosize=True,
                                                    margin=go.layout.Margin(
                                                        l=20,
                                                        r=20,
                                                        b=20,
                                                        t=20,
                                                        pad=0,
                                                    ),
                                                ),
                                            ),
                                        ),
                                        width=6,
                                    ),
                                    dbc.Col(
                                        dcc.Graph(
                                            id="heatmap",
                                            figure=go.Figure(
                                                go.Heatmap(),
                                                layout=go.Layout(
                                                    autosize=True,
                                                    margin=go.layout.Margin(
                                                        l=20,
                                                        r=20,
                                                        b=20,
                                                        t=20,
                                                        pad=0,
                                                    ),
                                                ),
                                            ),
                                        ),
                                        width=6,
                                    ),
                                ]
                            ),
                        ]
                    ),
                ],
            )
        ]
    )
