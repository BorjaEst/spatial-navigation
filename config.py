"""
Configuration module for the spatial-navigation project.

This module sets up the default data path for the project by reading the
environment variables. If a environment variable is not set, it defaults.

Attributes:
    DATA_PATH (str): The path to the data directory, either from the
"""

import os
from pathlib import Path

DATA_PATH = os.getenv("DATA_PATH", "data")
data_path = Path(DATA_PATH)
