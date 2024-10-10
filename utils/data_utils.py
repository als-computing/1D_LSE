import numpy as np


def generate_random_spectra():
    """
    Generates random Gaussian spectra data.
    """
    data = []
    for _ in range(20):
        mean = np.random.uniform(0, 1, 1)
        sigma = np.random.uniform(0.1, 0.5, 1)
        x = np.linspace(0, 1, 100)
        y = np.exp(-((x - mean) ** 2) / (2 * sigma**2))
        data.append(y.tolist())
    return data


def generate_random_latent_vectors():
    """
    Generates random latent vectors.
    """
    cluster1 = np.random.normal(0, 1, (10, 2))
    cluster2 = np.random.normal(2, 1, (10, 2))
    return cluster1.tolist() + cluster2.tolist()
