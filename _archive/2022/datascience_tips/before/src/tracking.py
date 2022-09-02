from abc import ABC, abstractmethod
from dataclasses import dataclass
from numbers import Real
from pathlib import Path
from typing import Union, Tuple

import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from torch.utils.tensorboard import SummaryWriter


@dataclass(frozen=True)
class Stage:
    TRAIN: str = 'train'
    TEST: str = 'test'
    VAL: str = 'val'


class ExperimentTracker(ABC):
    stage: str

    @abstractmethod
    def add_batch_metric(self, name: str, value: Real, step: int):
        """Implements logging a batch-level metric."""

    @abstractmethod
    def add_epoch_metric(self, name: str, value: Real, step: int):
        """Implements logging a epoch-level metric."""

    @abstractmethod
    def add_epoch_confusion_matrix(self, y_true: np.array, y_pred: np.array, step: int):
        """Implements logging a confusion matrix at epoch-level."""

    @abstractmethod
    def add_hparams(self, hparams: dict[str, Union[str, Real]], metrics: dict[str, Real]):
        """Implements logging hyperparameters."""

    def add_batch_metrics(self, values: dict[str, Real], step: int):
        for name, value in values.items():
            self.add_batch_metric(name, value, step)

    def add_epoch_metrics(self, values: dict[str, Real], step: int):
        for name, value in values.items():
            self.add_epoch_metric(name, value, step)


class TensorboardExperiment(ExperimentTracker):

    def __init__(self, log_dir: str, create=True):
        self._validate_log_dir(log_dir, create=create)
        self._writer = SummaryWriter(log_dir=log_dir)
        plt.ioff()

    def set_stage(self, stage: str):
        self.stage = stage
        return self

    def flush(self):
        self._writer.flush()

    @staticmethod
    def _validate_log_dir(log_dir, create=True):
        log_dir = Path(log_dir).resolve()
        if log_dir.exists():
            return
        elif not log_dir.exists() and create:
            log_dir.mkdir(parents=True)
        else:
            raise NotADirectoryError(f'log_dir {log_dir} does not exist.')

    def add_batch_metric(self, name: str, value: Real, step: int):
        tag = f'{self.stage}/batch/{name}'
        self._writer.add_scalar(tag, value, step)

    def add_epoch_metric(self, name: str, value: Real, step: int):
        tag = f'{self.stage}/epoch/{name}'
        self._writer.add_scalar(tag, value, step)

    def add_epoch_confusion_matrix(self, y_true: list[np.array], y_pred: list[np.array], step: int):
        y_true, y_pred = self.collapse_batches(y_true, y_pred)
        fig = self.create_confusion_matrix(y_true, y_pred, step)
        tag = f'{self.stage}/epoch/confusion_matrix'
        self._writer.add_figure(tag, fig, step)

    @staticmethod
    def collapse_batches(y_true: list[np.array], y_pred: list[np.array]) -> Tuple[np.ndarray, np.ndarray]:
        return np.concatenate(y_true), np.concatenate(y_pred)

    def create_confusion_matrix(self, y_true: np.array, y_pred: np.array, step: int) -> plt.Figure:
        cm = ConfusionMatrixDisplay(confusion_matrix(y_true, y_pred)).plot(cmap='Blues')
        fig: plt.Figure = cm.figure_
        ax: plt.Axes = cm.ax_
        ax.set_title(f'{self.stage.title()} Epoch: {step}')
        return fig

    def add_hparams(self, hparams: dict[str, Union[str, Real]], metrics: dict[str, Real]):
        _metrics = self._validate_hparam_metric_keys(metrics)
        self._writer.add_hparams(hparams, _metrics)

    @staticmethod
    def _validate_hparam_metric_keys(metrics):
        _metrics = metrics.copy()
        prefix = 'hparam/'
        for name in _metrics.keys():
            if not name.startswith(prefix):
                _metrics[f'{prefix}{name}'] = _metrics[name]
                del _metrics[name]
        return _metrics
