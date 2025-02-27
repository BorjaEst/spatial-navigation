"""Configuration module for the spatial-navigation project."""

import os
import tomllib
from pathlib import Path

DATA_PATH = os.getenv("DATA_PATH", "data")
data_path = Path(DATA_PATH)

EXPERIMENTS_PATH = os.getenv("EXPERIMENTS_PATH", "experiments")
experiments = Path(EXPERIMENTS_PATH)


def load_experiment(file_path: Path):
    """Load the experiment configuration from a TOML file."""
    with open(file_path, "rb") as file:
        return tomllib.load(file)
