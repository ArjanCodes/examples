import hydra
import torch
from hydra.core.config_store import ConfigStore
from omegaconf import OmegaConf

from config import MNISTConfig
from ds.dataset import create_dataloader
from ds.models import LinearNet
from ds.runner import Runner, run_epoch
from ds.tracking import TensorboardExperiment

cs = ConfigStore.instance()
cs.store(name="mnist_config", node=MNISTConfig)


@hydra.main(config_path="conf", config_name="config")
def main(cfg: MNISTConfig) -> None:
    print(OmegaConf.to_yaml(cfg))

    # Model and Optimizer
    model = LinearNet()
    optimizer = torch.optim.Adam(model.parameters(), lr=cfg.params.lr)

    # Create the data loaders

    test_loader = create_dataloader(
        batch_size=cfg.params.batch_size,
        root_path=cfg.paths.data,
        data_file=cfg.files.test_data,
        label_file=cfg.files.test_labels,
    )
    train_loader = create_dataloader(
        batch_size=cfg.params.batch_size,
        root_path=cfg.paths.data,
        data_file=cfg.files.train_data,
        label_file=cfg.files.train_labels,
    )

    # Create the runners
    test_runner = Runner(test_loader, model)
    train_runner = Runner(train_loader, model, optimizer)

    # Setup the experiment tracker
    tracker = TensorboardExperiment(log_path=cfg.paths.log)

    # Run the epochs
    for epoch_id in range(cfg.params.epoch_count):
        run_epoch(test_runner, train_runner, tracker, epoch_id)

        # Compute Average Epoch Metrics
        summary = ", ".join(
            [
                f"[Epoch: {epoch_id + 1}/{cfg.params.epoch_count}]",
                f"Test Accuracy: {test_runner.avg_accuracy: 0.4f}",
                f"Train Accuracy: {train_runner.avg_accuracy: 0.4f}",
            ]
        )
        print("\n" + summary + "\n")

        # Reset the runners
        train_runner.reset()
        test_runner.reset()

        # Flush the tracker after every epoch for live updates
        tracker.flush()


if __name__ == "__main__":
    main()
