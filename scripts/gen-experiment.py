# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name

import datetime as dt
import logging
import pickle
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich.logging import RichHandler

from spnav import Block, Experiment, config
from spnav import control as controllers
from spnav import maps

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
    out_path = config.data_path / f"{args.output_file}.npy"
    exp_path = config.experiments / f"{args.experiment}.toml"

    # Prepare the control for the experiment
    logger.info("Setting up the control for the experiment")
    control = controllers.ManualControl

    # Load the experiment configuration
    logger.info("Loading experiment configuration from file %s", exp_path)
    exp_cfg = config.load_experiment(exp_path)

    # get the map environment
    logger.info("Preparing map environment: %s", exp_cfg["experiment"])
    experiment = Experiment(
        name=exp_cfg["experiment"]["name"],
        blocks=[gen_blk(control, **kwds) for kwds in exp_cfg["block"]],
    )

    # save experiment to a file
    logger.info("Saving environment to file %s", out_path)
    with open(out_path, "wb") as file:
        pickle.dump(experiment, file)


def gen_blk(ctrl, mace: str, trajectories: int) -> Block:
    """Generate a block with the MACE and trajectories."""
    mace_env = maps.get_map(mace, render_mode="human")

    # Run the control for the trajectories in the MACE
    for _ in range(trajectories):
        ctrl(mace_env, seed=42).start()
    mace_env.close()

    # Return the block with the trajectories
    return Block(episode=mace_env.trajectories, mace=mace)


if __name__ == "__main__":
    main(args=Arguments())  # type: ignore
