import numpy as np
import plotly.graph_objects as go


def generate_heatmap_plot(selected_images, display_option):
    if len(selected_images) == 0:
        return go.Figure(
            layout=dict(
                autosize=True,
                margin=go.layout.Margin(l=20, r=20, b=20, t=20, pad=0),
            ),
        )
    selected_images = np.array(selected_images)
    x = np.arange(selected_images.shape[1])
    if selected_images.ndim == 1:
        heatmap_data = go.Scatter(x=x, y=selected_images)
    elif display_option == "mean":
        heatmap_data = go.Scatter(x=x, y=np.mean(selected_images, axis=0))
    elif display_option == "sigma":
        heatmap_data = go.Scatter(x=x, y=np.std(selected_images, axis=0))

    return go.Figure(
        data=heatmap_data,
        layout=dict(
            autosize=True,
            margin=go.layout.Margin(l=20, r=20, b=20, t=20, pad=0),
        ),
    )


def generate_scattergl_plot(
    x_coords,
    y_coords,
    labels,
    label_to_string_map,
    show_legend=False,
    custom_indices=None,
):
    """
    Generates a two dimensional Scattergl plot.

    Parameters:
    x_coords (list): The x-coordinates of the points.
    y_coords (list): The y-coordinates of the points.
    labels (list): The labels of the points.
    label_to_string_map (dict): A mapping from labels to strings.
    show_legend (bool, optional): Whether to show a legend. Default is False.
    custom_indices (list, optional): Custom indices for the points. Default is None.

    Returns:
    go.Figure: The generated Scattergl plot.
    """
    # Create a set of unique labels
    unique_labels = set(labels)

    # Create a trace for each unique label
    traces = []
    for label in unique_labels:
        # Find the indices of the points with the current label
        trace_indices = [i for i, l in enumerate(labels) if l == label]
        trace_x = [x_coords[i] for i in trace_indices]
        trace_y = [y_coords[i] for i in trace_indices]

        if custom_indices is not None:
            trace_custom_indices = [custom_indices[i] for i in trace_indices]
        else:
            trace_custom_indices = trace_indices

        traces.append(
            go.Scattergl(
                x=trace_x,
                y=trace_y,
                customdata=np.array(trace_custom_indices).reshape(-1, 1),
                mode="markers",
                name=str(label_to_string_map[label]),
            )
        )

    # Create the plot with the scatter plot traces
    fig = go.Figure(data=traces)
    if show_legend:
        fig.update_layout(
            legend=dict(
                x=0,
                y=1,
                bgcolor="rgba(255, 255, 255, 0.9)",
                bordercolor="rgba(255, 255, 255, 0.9)",
                orientation="h",
            )
        )
    return fig


def generate_scatter3d_plot(
    x_coords,
    y_coords,
    z_coords,
    labels,
    label_to_string_map,
    show_legend=False,
    custom_indices=None,
):
    """
    Generates a three-dimensional Scatter3d plot.

    Parameters:
    x_coords (list): The x-coordinates of the points.
    y_coords (list): The y-coordinates of the points.
    z_coords (list): The z-coordinates of the points.
    labels (list): The labels of the points.
    label_to_string_map (dict): A mapping from labels to strings.
    show_legend (bool, optional): Whether to show a legend. Default is False.
    custom_indices (list, optional): Custom indices for the points. Default is None.

    Returns:
    go.Figure: The generated Scatter3d plot.
    """
    # Create a set of unique labels
    unique_labels = set(labels)

    # Create a trace for each unique label
    traces = []
    for label in unique_labels:
        # Find the indices of the points with the current label
        trace_indices = [i for i, l in enumerate(labels) if l == label]
        trace_x = [x_coords[i] for i in trace_indices]
        trace_y = [y_coords[i] for i in trace_indices]
        trace_z = [z_coords[i] for i in trace_indices]

        if custom_indices is not None:
            trace_custom_indices = [custom_indices[i] for i in trace_indices]
        else:
            trace_custom_indices = trace_indices

        traces.append(
            go.Scatter3d(
                x=trace_x,
                y=trace_y,
                z=trace_z,
                customdata=np.array(trace_custom_indices).reshape(-1, 1),
                mode="markers",
                name=str(label_to_string_map[label]),
                marker=dict(size=3),
            )
        )

    # Create the plot with the Scatter3d traces
    fig = go.Figure(data=traces)
    if show_legend:
        fig.update_layout(
            legend=dict(
                x=0,
                y=1,
                bgcolor="rgba(255, 255, 255, 0.9)",
                bordercolor="rgba(255, 255, 255, 0.9)",
                orientation="h",
            )
        )
    return fig


def generate_scatter_plot(
    latent_vectors,
    n_components,
    cluster_selection=-1,  # "All"
    clusters=None,
    cluster_names=None,
    label_selection=-2,  # "All"
    labels=None,
    label_names=None,
    color_by="label",
):
    """
    Generate data for a plot according to the provided selection options:
    1. all clusters & all labels
    2. all clusters and selected labels
    3. all labels and selected clusters
    4. selected clusters and selected labels

    Parameters:
    latent_vectors (numpy.ndarray, Nx2, floats): [Description]
    n_components: number principal components
    cluster_selection (int): The cluster w want to select. Defaults to -1: all clusters
    clusters (numpy.ndarray, N, ints optional): The cluster number for each data point
    cluster_names (dict, optional): [Description]. A dictionary with cluster names
    label_selection (str, optional): Which label to select. Defaults to -2: all labels. -1 mean Unlabeled
    labels (numpy.ndarray, N, int, optional): The current labels Defaults to None.
    label_names (dict, optional): A dictionary that relates label number to name.
    color_by (str, optional): Determines if we color by label or cluster. Defaults to None.

    Returns:
    plotly.scattergl: A plot as specified.
    """
    # case:
    #  all data: cluster_selection =-1, label_selection=-2
    #  all clusters, selected labels
    #  all labels, selected clusters

    latent_vectors = np.array(latent_vectors)

    if labels is None:
        labels = np.full((latent_vectors.shape[0],), -1)

    vals_names = {}
    if color_by == "cluster":
        vals = clusters
        vals_names = cluster_names
    else:
        vals = labels
        if label_names is not None:
            vals_names = {value: key for key, value in label_names.items()}
        vals_names[-1] = "Unlabeled"

    if (cluster_selection == -1) & (label_selection == -2):
        if n_components == 2:
            scatter_data = generate_scattergl_plot(
                latent_vectors[:, 0], latent_vectors[:, 1], vals, vals_names
            )
        else:
            scatter_data = generate_scatter3d_plot(
                latent_vectors[:, 0],
                latent_vectors[:, 1],
                latent_vectors[:, 2],
                vals,
                vals_names,
            )
        fig = go.Figure(scatter_data)
        fig.update_layout(
            dragmode="lasso",
            margin=go.layout.Margin(l=20, r=20, b=20, t=20, pad=0),
            legend=dict(tracegroupgap=20),
        )
        return fig

    selected_indices = None
    clusters = np.array(clusters)
    labels = np.array(labels)
    if (cluster_selection == -1) & (label_selection != -2):  # all clusters
        if label_selection != -1:
            label_selection = label_names[label_selection]
        selected_indices = np.where(labels == label_selection)[0]

    if (label_selection == -2) & (cluster_selection > -1):  # all clusters
        selected_indices = np.where(clusters == cluster_selection)[0]

    if (label_selection != -2) & (cluster_selection > -1):
        if label_selection != -1:
            selected_labels = label_names[label_selection]
            selected_indices = np.where(
                (clusters == cluster_selection) & (labels == selected_labels)
            )[0]
        else:
            selected_indices = np.where((clusters == cluster_selection))[0]

    vals = np.array(vals)
    if n_components == 2:
        scatter_data = generate_scattergl_plot(
            latent_vectors[selected_indices, 0],
            latent_vectors[selected_indices, 1],
            vals[selected_indices],
            vals_names,
            custom_indices=selected_indices,
        )
    elif n_components == 3:
        scatter_data = generate_scatter3d_plot(
            latent_vectors[selected_indices, 0],
            latent_vectors[selected_indices, 1],
            latent_vectors[selected_indices, 2],
            vals[selected_indices],
            vals_names,
            custom_indices=selected_indices,
        )

    fig = go.Figure(scatter_data)
    fig.update_layout(
        dragmode="lasso",
        margin=go.layout.Margin(l=20, r=20, b=20, t=20, pad=0),
        legend=dict(tracegroupgap=20),
    )
    return fig
