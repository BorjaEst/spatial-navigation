"""Package for spatial navigation experiments."""

import dataclasses as dc
import logging
import pickle
from typing import Any, Iterable

import ehc_sn as ehc
from ehc_sn import Episode
from minigrid.manual_control import ManualControl

from spnav import config
from spnav.env import BlockSettings, ExperimentSettings, Mace

logger = logging.getLogger(__name__)


@dc.dataclass(init=False)
class Block:  # pylint: disable=too-few-public-methods
    """Block class to hold the episode with information."""

    mace: str
    configuration: BlockSettings
    episodes: list[ehc.Episode]

    def __init__(self, name: str, **options: dict[str, Any]) -> None:
        self.mace = name
        self.configuration = BlockSettings(**options)  # type: ignore
        environment = Mace(name, settings=self.configuration)
        self.episodes = run_mace(environment)

    def __iter__(self) -> Iterable[Episode]:
        """Iterate over the episodes of the block."""
        return iter(self.episodes)

    def __repr__(self):
        return (
            f"Block:{self.mace} ("
            + f"len={len(self.episodes)}; "
            + f"{self.configuration})"
        )


@dc.dataclass(init=False)
class Experiment:  # pylint: disable=too-few-public-methods
    """Experiment class to hold the blocks of an experiment."""

    name: str
    configuration: ExperimentSettings
    blocks: list[Block]

    def __init__(self, name: str, **options: dict[str, Any]) -> None:
        self.name = name
        self.configuration = ExperimentSettings(**options["experiment"])
        self.blocks = [
            self.block(mace_name, **options["blocks"][mace_name])
            for mace_name in options["blocks"]
        ]

    def __iter__(self) -> Iterable[Block]:
        """Iterate over the blocks of the experiment."""
        return iter(self.blocks)

    def block(self, name: str, **options: dict[str, str]) -> Block:
        """Return the block configurations."""
        block_configuration = {**self.configuration.model_dump(), **options}
        return Block(name, **block_configuration)

    def __repr__(self):
        return (
            f"Experiment:{self.name} ("
            + f"n_blocks={len(self.blocks)}; "
            + f"{self.configuration})"
        )


def run_mace(env: Mace) -> list[Episode]:
    """Run the MACE environment with the manual control."""
    try:
        ManualControl(env).start()
    except StopIteration:
        logger.info("End of the mace simulation")
    return env.episodes


def save_experiment(experiment: Experiment, filename: str) -> None:
    """Save the experiment configuration."""
    file_path = config.data_path / f"{filename}.pickle"
    with file_path.open("wb") as file:
        pickle.dump(experiment, file)


def save_block(block: Block, filename: str) -> None:
    """Save the block configuration."""
    file_path = config.data_path / f"{filename}.pickle"
    with file_path.open("wb") as file:
        pickle.dump(block, file)


def load_experiment(filename: str) -> Experiment:
    """Load the experiment configuration."""
    file_path = config.data_path / f"{filename}.pickle"
    with file_path.open("rb") as file:
        return pickle.load(file)


def load_block(filename: str) -> Block:
    """Load the block configuration."""
    file_path = config.data_path / f"{filename}.pickle"
    with file_path.open("rb") as file:
        return pickle.load(file)
