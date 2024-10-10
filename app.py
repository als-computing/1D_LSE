import dash_bootstrap_components as dbc
from dash import Dash, html

from callbacks.image_viewer import update_heatmap, update_scatter_plot  # noqa: F401
from callbacks.update_data import update_data  # noqa: F401
from components.controls import layout as controls_layout
from components.image_viewer import layout as image_panel

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div(
    dbc.Container(
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        controls_layout(),
                        width=4,
                        style={"display": "flex", "margin-top": "1em"},
                    ),
                    dbc.Col(image_panel(), width=8),
                ]
            ),
        ]
    )
)


if __name__ == "__main__":
    app.run_server(port=8052, debug=True)
