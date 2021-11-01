import hydra
from hydra.core.config_store import ConfigStore
from omegaconf import OmegaConf

from config import MNISTConfig

cs = ConfigStore.instance()
cs.store(name="config", node=MNISTConfig)


@hydra.main(config_path="conf", config_name="config")
def main(cfg: MNISTConfig) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    main()
