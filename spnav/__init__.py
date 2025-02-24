"""Package for spatial navigation experiments."""

import dataclasses as dc

from ehc_sn import Episode


@dc.dataclass
class Block:  # pylint: disable=too-few-public-methods
    """Block class to hold the episode with information."""

    episode: Episode
    mace: str

    def __iter__(self):
        """Iterate over the episodes of the block."""
        return iter(self.episode)


@dc.dataclass
class Experiment:  # pylint: disable=too-few-public-methods
    """Experiment class to hold the blocks of an experiment."""

    name: str
    blocks: list[Block]

    def __iter__(self):
        """Iterate over the blocks of the experiment."""
        return iter(self.blocks)
