import dash_bootstrap_components as dbc
from dash import dcc, html


def layout():
    return html.Div(
        [
            html.P("Data Access / Controls"),
            dcc.RadioItems(
                id="mean-std-toggle",
                options=[
                    {"label": "Mean", "value": "mean"},
                    {"label": "Standard Deviation", "value": "sigma"},
                ],
                value="mean",
                style={"min-width": "250px"},
                className="mb-2",
            ),
            dbc.Button("Generate new data", id="reset-button", color="primary"),
            dcc.Store("data", data=[]),
            dcc.Store("latent-vectors", data=[]),
        ]
    )
