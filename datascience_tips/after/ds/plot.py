import matplotlib.pyplot as plt
import numpy as np


def plot_sample_image(arr: np.ndarray, label: int) -> plt.Figure:
    fig, ax = plt.subplots(1, 1)
    ax.imshow(arr, cmap='gray')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f'Label: {label:d}')
    plt.show()
    return fig
