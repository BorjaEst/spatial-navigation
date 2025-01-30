"""
This script initializes and runs a spatial navigation application using a 
specified map and logging level.

Modules:
    argparse: Provides command-line argument parsing functionality.
    logging: Provides logging functionality.
    ehc_sn.control.ManualControl: Provides manual control for the map environment.
    maps: Provides functionality to retrieve map environments.

Example:
    To run the script with a specified map and logging level:
        python main.py --map example_map --log-level DEBUG
"""

import argparse
import datetime as dt
import logging

import numpy as np
import pygame
from ehc_sn.control import ManualControl

import config
import maps

parser = argparse.ArgumentParser(prog=__doc__)
parser.add_argument(
    "--map",
    type=str,
    required=True,
    help="Input map as a string",
)
parser.add_argument(
    "--log-level",
    type=str,
    choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    default="INFO",
    help="Set the logging level",
)


def main(args):
    """
    Main function to initialize the spatial navigation application.

    Args:
        args: Command-line arguments containing the following attributes:
            map (str): The map name for the navigation.
            log_level (str): The logging level to be set 7
                (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').

    Returns:
        None
    """
    map_name = args.map
    log_level = args.log_level

    logging.basicConfig(level=getattr(logging, log_level))

    # Log the map input and log level
    logger = logging.getLogger(__name__)
    logger.debug("Map input received: %s", map_name)
    logger.debug("Log level set to: %s", log_level)

    # get the map environment
    logger.info("Getting map environment: %s", map_name)
    map_env = maps.get_map(map_name, render_mode="human")

    # enable manual control for testing
    try:
        logger.info("Starting manual control")
        manual_control = ManualControl(map_env, seed=42)
        manual_control.start()
    except pygame.error as error:
        logger.error("Pygame error: %s", error)
    finally:
        logger.info("Closing map environment")
        map_env.close()

    # save trajectories to a file
    logger.info("Saving environment to a file")
    timestamp = dt.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"{config.DATA_PATH}/episodes_{timestamp}.npy"
    episodes = np.array(map_env.trajectories, dtype=object)
    np.save(file_name, episodes, allow_pickle=True)


if __name__ == "__main__":
    _arguments = parser.parse_args()
    main(_arguments)
