from dash import Input, Output, callback, no_update

from utils.data_utils import generate_random_latent_vectors, generate_random_spectra


@callback(
    Output("data", "data"),
    Output("latent-vectors", "data"),
    Input("reset-button", "n_clicks"),
)
def update_data(n_clicks):
    """
    Updates the data store with new data.
    """
    if n_clicks:
        data = generate_random_spectra()
        latent_vectors = generate_random_latent_vectors()
        return data, latent_vectors
    return no_update
