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

from spnav import config, maps
from spnav.control import ManualControl

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
logger = logging.getLogger(__name__)


class Arguments(BaseSettings):
    """
    This script provides a command-line interface to produce a navigation
    experiment. It uses an experiment configuration file to set the
    environment and parameters to generate an output file with the
    Experiment instance containing the trajectories and other information.
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
    experiment: str = Field(
        description="Experiment TOML name from 'experiments' folder.",
        examples=["example_experiment"],
    )
    output_file: str = Field(
        default=f"experiment_{dt.datetime.now().strftime('%Y%m%d%H%M%S')}",
        description="Output file name for saving trajectories.",
    )


def main(args: Arguments):
    """Main function to generate the spatial navigation experiment."""

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
    experiment = None  # TODO: Generate the experiment

    # save experiment to a file
    logger.info("Saving environment to file %s", output)
    np.save(output, experiment, allow_pickle=True)


if __name__ == "__main__":
    main(args=Arguments())  # type: ignore
