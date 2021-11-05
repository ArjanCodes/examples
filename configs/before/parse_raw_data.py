import os
import shutil
import pathlib
from typing import Iterable, Tuple

import numpy as np
from PIL import Image
from tqdm import tqdm

from ds.load_data import load_image_data, load_label_data

RAW_DATA = "./data/raw"
TEST_DATA_RAW = pathlib.Path(f"{RAW_DATA}/t10k-images-idx3-ubyte.gz")
TEST_LABELS_RAW = pathlib.Path(f"{RAW_DATA}/t10k-labels-idx1-ubyte.gz")
TRAIN_DATA_RAW = pathlib.Path(f"{RAW_DATA}/train-images-idx3-ubyte.gz")
TRAIN_LABELS_RAW = pathlib.Path(f"{RAW_DATA}/train-labels-idx1-ubyte.gz")

PROCESSED_DATA = './data/processed'
TEST_DIR_PROCESSED = pathlib.Path(f"{PROCESSED_DATA}/test")
TRAIN_DIR_PROCESSED = pathlib.Path(f"{PROCESSED_DATA}/tain")


def main():
    make_tree(TRAIN_DIR_PROCESSED, reset=True)
    make_tree(TEST_DIR_PROCESSED, reset=True)

    save_dataset_to_png(
        TRAIN_DIR_PROCESSED, 
        zip(load_image_data(TRAIN_DATA_RAW), load_label_data(TRAIN_LABELS_RAW))
    )
    save_dataset_to_png(
        TEST_DIR_PROCESSED, 
        zip(load_image_data(TEST_DATA_RAW), load_label_data(TEST_LABELS_RAW))
    )


def make_tree(root: pathlib.Path, reset: bool = False) -> None:
    if reset:
        reset_tree(root)
    for child in range(10):
        child = pathlib.Path(str(child))
        if not child.exists():
            os.makedirs(root / child)


def reset_tree(root: pathlib.Path) -> None:
    print('Resetting tree.')
    shutil.rmtree(root, ignore_errors=True)


def save_dataset_to_png(
    root: pathlib.Path, array: Iterable[Tuple[np.ndarray, np.ndarray]]
) -> None:
    for i, xy in enumerate(tqdm(tuple(array), ncols=80)):
        save_xy_to_png(root, xy, str(i))


def save_xy_to_png(
    root: pathlib.Path, xy: Tuple[np.ndarray, np.ndarray], name: str
) -> None:
    x, y = xy
    Image.fromarray(x).save(root / str(int(y)) / f'{name}.jpg')


if __name__ == '__main__':
    main()
