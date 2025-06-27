"""main."""
import hydra
from omegaconf import DictConfig


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig) -> None:
    print(f"running with config: {cfg}")
    print(f"model name is {cfg.model.name}")
    print(f"clip_frames is {cfg.training.dataloader.clip_frames}")

if __name__ == "__main__":
    main()
