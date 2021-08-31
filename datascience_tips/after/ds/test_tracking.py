import shutil
import time
import unittest
from pathlib import Path

import numpy as np

from tracking import Stage, TensorboardExperiment


def tear_down_runs_dir(log_dir):
    log_dir = Path(log_dir)
    if log_dir.exists():
        shutil.rmtree(log_dir, ignore_errors=True)


class TestTensorboardExperimentLogDir(unittest.TestCase):
    def setUp(self):
        self.log_dir = "runs"

    def tearDown(self):
        tear_down_runs_dir(self.log_dir)

    def test_sets_correct_log_dir(self):
        writer = TensorboardExperiment(log_dir=self.log_dir).set_stage(Stage.TRAIN)
        self.assertEqual(writer._writer.log_dir, self.log_dir)

    def test_creates_correct_log_dir(self):
        _ = TensorboardExperiment(log_dir=self.log_dir).set_stage(Stage.TRAIN)
        self.assertTrue(Path(self.log_dir).exists())

    def test_raise_error_if_log_dir_does_not_exist_and_do_not_allow_creation(self):
        with self.assertRaises(NotADirectoryError):
            _ = TensorboardExperiment(log_dir=self.log_dir, create=False).set_stage(
                Stage.TRAIN
            )


class TestTensorboardExperimentBatchMetrics(unittest.TestCase):
    def setUp(self):
        self.log_dir = "runs"
        self.writer = TensorboardExperiment(log_dir=self.log_dir).set_stage(Stage.TRAIN)

    def tearDown(self):
        self.writer._writer.flush()
        tear_down_runs_dir(self.log_dir)

    def test_add_batch_metric_int(self):
        self.writer.add_batch_metric(name="test_metric", value=1, step=1)

    def test_add_batch_metric_float(self):
        self.writer.add_batch_metric(name="test_metric", value=1.3, step=1)

    def test_add_batch_metric_complex_int(self):
        with self.assertRaises(TypeError):
            self.writer.add_batch_metric(name="test_metric", value=7j, step=1)

    def test_add_batch_metric_complex_float(self):
        with self.assertRaises(TypeError):
            self.writer.add_batch_metric(name="test_metric", value=3.6j, step=1)

    def test_add_batch_metric_real_and_complex(self):
        with self.assertRaises(TypeError):
            self.writer.add_batch_metric(name="test_metric", value=2.1 + 3.6j, step=1)

    class TestTensorboardExperimentEpochMetrics(unittest.TestCase):
        def setUp(self):
            self.log_dir = "runs"
            self.writer = TensorboardExperiment(log_dir=self.log_dir).set_stage(
                Stage.TEST
            )

        def tearDown(self):
            self.writer._writer.flush()
            tear_down_runs_dir(self.log_dir)

        def test_add_epoch_metric_int(self):
            self.writer.add_epoch_metric(name="test_metric", value=1, step=1)

        def test_add_epoch_metric_float(self):
            self.writer.add_epoch_metric(name="test_metric", value=1.3, step=1)

        def test_add_epoch_metric_complex_int(self):
            with self.assertRaises(TypeError):
                self.writer.add_epoch_metric(name="test_metric", value=7j, step=1)

        def test_add_epoch_metric_complex_float(self):
            with self.assertRaises(TypeError):
                self.writer.add_epoch_metric(name="test_metric", value=3.6j, step=1)

        def test_add_epoch_metric_real_and_complex(self):
            with self.assertRaises(TypeError):
                self.writer.add_epoch_metric(
                    name="test_metric", value=2.1 + 3.6j, step=1
                )


class TestTensorboardExperimentConfusionMatrix(unittest.TestCase):
    def setUp(self):
        self.log_dir = "runs"
        self.writer = TensorboardExperiment(log_dir=self.log_dir).set_stage(Stage.VAL)

    def tearDown(self):
        tear_down_runs_dir(self.log_dir)

    def test_add_confusion_matrix(self):
        y_true = [np.array([i]) for i in [0, 1, 2]]
        y_pred = [np.array([i]) for i in [0, 0, 2]]
        self.writer.add_epoch_confusion_matrix(y_true, y_pred, step=10)

    def test_add_confusion_matrix_raises_error_with_unequal_vectors(self):
        y_true_unequal = [np.array([i]) for i in [0, 1, 2, 2]]
        y_pred = [np.array([i]) for i in [0, 0, 2]]
        with self.assertRaises(ValueError):
            self.writer.add_epoch_confusion_matrix(y_true_unequal, y_pred, step=10)


if __name__ == "__main__":
    unittest.main()
