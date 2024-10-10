from dash import Input, Output, State, callback

from utils.plot_utils import generate_heatmap_plot, generate_scatter_plot


@callback(
    Output("scatter", "figure"),
    Input("latent-vectors", "data"),
    State("scatter", "figure"),
)
def update_scatter_plot(
    latent_vectors: list,
    current_figure: dict,
):
    """
    Updates the scatter plot with the latent vectors.
    """
    fig = generate_scatter_plot(latent_vectors, 2)
    fig.update_xaxes(range=current_figure["layout"]["xaxis"]["range"])
    fig.update_yaxes(range=current_figure["layout"]["yaxis"]["range"])
    return fig


@callback(
    Output("heatmap", "figure"),
    Input("scatter", "clickData"),
    Input("scatter", "selectedData"),
    Input("mean-std-toggle", "value"),
    State("data", "data"),
    prevent_initial_call=True,
)
def update_heatmap(
    click_data: dict,
    selected_data: dict,
    display_option: bool,
    data: dict,
):
    # user select a group of points
    if selected_data is not None and len(selected_data["points"]) > 0:
        selected_indices = [
            point["customdata"][0] for point in selected_data["points"]
        ]  # Access customdata for the original indices
        selected_images = [data[i] for i in selected_indices]

    elif click_data is not None and len(click_data["points"]) > 0:
        selected_images = data[click_data["points"][0]["customdata"][0]]
    else:
        selected_images = []

    fig = generate_heatmap_plot(selected_images, display_option)
    return fig
