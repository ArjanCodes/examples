import numpy as np
import torch
from sklearn.metrics import accuracy_score
from tqdm import tqdm

from src.dataset import get_train_dataloader, get_test_dataloader
from src.metrics import Metric
from src.models import LinearNet
from src.tracking import TensorboardExperiment, Stage
from src.utils import generate_tensorboard_experiment_directory

# Hyperparameters
hparams = {
    'EPOCHS': 20,
    'LR': 5e-5,
    'OPTIMIZER': 'Adam',
    'BATCH_SIZE': 128
}

# Data
train_loader = get_train_dataloader(batch_size=hparams.get('BATCH_SIZE'))
test_loader = get_test_dataloader(batch_size=hparams.get('BATCH_SIZE'))

# Model and Optimizer
model = LinearNet()
optimizer = torch.optim.Adam(model.parameters(), lr=hparams.get('LR'))

# Objective (loss) function
compute_loss = torch.nn.CrossEntropyLoss(reduction='mean')

# Metric Containers
train_accuracy = Metric()
test_accuracy = Metric()
y_true_batches = []
y_pred_batches = []

# Experiment Trackers
log_dir = generate_tensorboard_experiment_directory(root='./runs')
experiment = TensorboardExperiment(log_dir=log_dir)

# Batch Counters
test_batch = 0
train_batch = 0

for epoch in range(hparams.get('EPOCHS')):
    # Testing Loop
    for x_test, y_test in tqdm(test_loader, desc='Validation Batches', ncols=80):
        test_batch += 1
        test_batch_size = x_test.shape[0]
        test_pred = model(x_test)
        loss = compute_loss(test_pred, y_test)

        # Compute Batch Validation Metrics
        y_test_np = y_test.detach().numpy()
        y_test_pred_np = np.argmax(test_pred.detach().numpy(), axis=1)
        batch_test_accuracy = accuracy_score(y_test_np, y_test_pred_np)
        test_accuracy.update(batch_test_accuracy, test_batch_size)
        experiment.set_stage(Stage.VAL)
        experiment.add_batch_metric('accuracy', batch_test_accuracy, test_batch)
        y_true_batches += [y_test_np]
        y_pred_batches += [y_test_pred_np]

    # Training Loop
    for x_train, y_train in tqdm(train_loader, desc='Train Batches', ncols=80):
        train_batch += 1
        train_batch_size = x_train.shape[0]
        train_pred = model(x_train)
        loss = compute_loss(train_pred, y_train)

        # Compute Batch Training Metrics
        y_train_np = y_train.detach().numpy()
        y_train_pred_np = np.argmax(train_pred.detach().numpy(), axis=1)
        batch_train_accuracy = accuracy_score(y_train_np, y_train_pred_np)
        train_accuracy.update(batch_train_accuracy, train_batch_size)
        experiment.set_stage(Stage.TRAIN)
        experiment.add_batch_metric('accuracy', batch_train_accuracy, train_batch)

        # Reverse-mode AutoDiff (backpropagation)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    # Compute Average Epoch Metrics
    summary = ', '.join([
        f"[Epoch: {epoch + 1}/{hparams.get('EPOCHS')}]",
        f"Test Accuracy: {test_accuracy.average: 0.4f}",
        f"Train Accuracy: {train_accuracy.average: 0.4f}",
    ])
    print('\n' + summary + '\n')

    # Log Validation Epoch Metrics
    experiment.set_stage(Stage.VAL)
    experiment.add_epoch_metric('accuracy', test_accuracy.average, epoch)
    experiment.add_epoch_confusion_matrix(y_true_batches, y_pred_batches, epoch)

    # Log Validation Epoch Metrics
    experiment.set_stage(Stage.TRAIN)
    experiment.add_epoch_metric('accuracy', train_accuracy.average, epoch)

    # Reset metrics
    train_accuracy.reset()
    test_accuracy.reset()

experiment.flush()
