import argparse
import logging

from ehc_sn.control import ManualControl
import maps

parser = argparse.ArgumentParser(description="Process a map input.")
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
            log_level (str): The logging level to be set (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').

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
    map_env = maps.get_map(map_name)(render_mode="human")

    # enable manual control for testing
    manual_control = ManualControl(map_env, seed=42)
    manual_control.start()


if __name__ == "__main__":
    _arguments = parser.parse_args()
    main(_arguments)
