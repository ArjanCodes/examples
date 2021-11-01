from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset

from ds.load_data import load_image_data, load_label_data


class MNIST(Dataset[Any]):
    idx: int  # requested data index
    x: torch.Tensor
    y: torch.Tensor

    TRAIN_MAX = 255.0
    TRAIN_NORMALIZED_MEAN = 0.1306604762738429
    TRAIN_NORMALIZED_STDEV = 0.3081078038564622

    def __init__(self, data: np.ndarray, targets: np.ndarray):
        if len(data) != len(targets):
            raise ValueError(
                "data and targets must be the same length. "
                f"{len(data)} != {len(targets)}"
            )

        self.data = data
        self.targets = targets

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor]:
        x = self.get_x(idx)
        y = self.get_y(idx)
        return x, y

    def get_x(self, idx: int):
        self.idx = idx
        self.preprocess_x()
        return self.x

    def preprocess_x(self):
        self.x = self.data[self.idx].copy().astype(np.float64)
        self.x /= self.TRAIN_MAX
        self.x -= self.TRAIN_NORMALIZED_MEAN
        self.x /= self.TRAIN_NORMALIZED_STDEV
        self.x = self.x.astype(np.float32)
        self.x = torch.from_numpy(self.x)
        self.x = self.x.unsqueeze(0)

    def get_y(self, idx: int):
        self.idx = idx
        self.preprocess_y()
        return self.y

    def preprocess_y(self):
        self.y = self.targets[self.idx]
        self.y = torch.tensor(self.y, dtype=torch.long)


def create_dataloader(
    batch_size: int, data_path: Path, label_path: Path, shuffle: bool = True
) -> DataLoader[Any]:
    data = load_image_data(data_path)
    label_data = load_label_data(label_path)
    return DataLoader(
        dataset=MNIST(data, label_data),
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=0,
    )
