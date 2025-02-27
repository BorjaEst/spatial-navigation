# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name

import datetime as dt
import logging
import pickle
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich.logging import RichHandler

import spnav
from spnav import config, env

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
    experiment: str = Field(
        description="Experiment TOML name from 'experiments' folder.",
        examples=["example_experiment"],
    )
    block: str = Field(
        description="Block name from the mace to use.",
        examples=["mace_1"],
    )
    output_file: str = Field(
        default=f"block_{dt.datetime.now().strftime('%Y%m%d%H%M%S')}",
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
    out_path = config.data_path / f"{args.output_file}.pickle"
    exp_path = config.experiments / f"{args.experiment}.toml"

    # Load the experiment configuration
    logger.info("Loading experiment configuration from %s", exp_path)
    exp_cfg = config.load_experiment(exp_path)
    exp_settings = env.ExperimentSettings(**exp_cfg["experiment"])
    logger.debug("Experiment settings: %s", exp_settings)

    # Generate settings for the map
    logger.info("Generating settings from %s", args.block)
    options = {**exp_cfg["experiment"], **exp_cfg["blocks"][args.block]}
    logger.debug("Environment option: %s", options)

    # Generate the mace environment
    logger.info("Preparing mace environment: %s", args.block)
    block = spnav.Block(name=args.block, **options)
    logger.debug("Mace block object: %s", block)

    # Save trajectories to a file
    logger.info("Saving environment to file %s", out_path)
    with open(out_path, "wb") as file:
        pickle.dump(block, file)
    logger.debug("Environment saved successfully.")


if __name__ == "__main__":
    main(args=Arguments())  # type: ignore
