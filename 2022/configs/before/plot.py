import pathlib
from typing import Iterable, Tuple

import matplotlib.pyplot as plt
import numpy as np

from ds.load_data import load_image_data, load_label_data

DATA_DIR = pathlib.Path("./data/raw")
TEST_DATA = DATA_DIR / "t10k-images-idx3-ubyte.gz"
TEST_LABELS = DATA_DIR / "t10k-labels-idx1-ubyte.gz"
TRAIN_DATA = DATA_DIR / "train-images-idx3-ubyte.gz"
TRAIN_LABELS = DATA_DIR / "train-labels-idx1-ubyte.gz"

NUM_FIGS = 9
NUM_BLOCKS = 3


def main(dataset: str) -> None:
    data, labels = load(dataset)
    data, labels = sample(data, labels)
    plot(data, labels, dataset)


def load(dataset: str) -> Tuple[np.ndarray, np.ndarray]:
    dataset = {
        'train': {
            'data': TRAIN_DATA,
            'labels': TRAIN_LABELS,
        },
        'test': {
            'data': TEST_DATA,
            'labels': TEST_LABELS,
        }
    }[dataset]
    data = load_image_data(dataset['data'])
    labels = load_label_data(dataset['labels'])
    return data, labels


def sample(
    data: np.ndarray, labels: np.ndarray
) -> Tuple[Iterable[np.ndarray], Iterable[np.ndarray]]:
    idx = np.random.choice(range(data.shape[0]), size=NUM_FIGS)
    data = iter(data[idx])
    labels = iter(labels[idx])
    return data, labels


def plot(
    data: Iterable[np.ndarray], labels: Iterable[np.ndarray], dataset: str
) -> None:
    fig: plt.Figure
    ax: plt.Axes
    fig, axes = plt.subplots(NUM_BLOCKS, NUM_BLOCKS)
    axes = axes.flatten()

    for ax in axes:
        ax.imshow(next(data), cmap='Greys')
        ax.text(1, 5, str(next(labels)), color='red', fontsize=15)
        ax.set_xticks([])
        ax.set_yticks([])

    fig.suptitle(f'Dataset: {dataset}')
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.show()


if __name__ == '__main__':
    main(dataset='train')  # 'train' or 'test'
