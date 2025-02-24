# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name

import datetime as dt
import logging
from typing import Literal

import numpy as np
import pygame
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich.logging import RichHandler

from spnav import config, env
from spnav.control import ManualControl

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
logger = logging.getLogger(__name__)


class Arguments(BaseSettings):
    """
    This script provides a command-line interface to produce navigation
    sequences. It initializes the spatial navigation application using
    minigrid environments on the specified map.
    """  # Description for the script help message

    # Class attributes
    model_config = SettingsConfigDict(
        cli_prog_name="python -m scripts.gen-experiment",
        cli_parse_args=True,
    )

    # General settings
    log_level: LogLevel = Field(
        default="INFO",
        description="Set the logging level.",
    )

    # Script-specific settings
    map: str = Field(
        description="Input map as a string, e.g., 'example_map'.",
    )
    output_file: str = Field(
        default=f"episodes_{dt.datetime.now().strftime('%Y%m%d%H%M%S')}",
        description="Output file name for saving trajectories.",
    )


def main(args: Arguments):
    """Main function to run the spatial navigation application."""

    # Set the logging level from the arguments
    logging.basicConfig(
        handlers=[RichHandler(rich_tracebacks=True)],
        level=args.log_level,
    )

    # Load dataset and tools from the arguments
    logger.debug("Call arguments: %s", args)

    # Prepare internal variables
    output = config.data_path / f"{args.output_file}.npy"

    # get the map environment
    logger.info("Preparing map environment: %s", args.map)
    mace_env = maces.get_map(args.map, render_mode="human")

    # enable manual control for testing
    try:
        logger.info("Starting manual control")
        manual_control = ManualControl(mace_env, seed=42)
        manual_control.start()
    except pygame.error as error:  # pylint: disable=no-member
        logger.error("Pygame error: %s", error)
    finally:
        logger.info("Closing map environment")
        mace_env.close()

    # Collect and transform trajectories to episodes
    logger.info("Collecting trajectories")
    episodes = np.array(mace_env.trajectories, dtype=object)

    # save trajectories to a file
    logger.info("Saving environment to file %s", output)
    np.save(output, episodes, allow_pickle=True)


if __name__ == "__main__":
    main(args=Arguments())  # type: ignore
