"""Configuration module for the spatial-navigation project."""

import os
from pathlib import Path

DATA_PATH = os.getenv("DATA_PATH", "data")
data_path = Path(DATA_PATH)
