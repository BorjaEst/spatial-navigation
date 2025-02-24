"""
This module provides functionality to retrieve and initialize mace objects.

Modules:
    maces.example: Contains example mace definitions.

Functions:
    get_mace(mace_name, **options):
"""

from spnav.maces.example import example_mace
from spnav.maces import baseline

_maces = {
    "example": example_mace,
    "baseline_1": baseline.mace_1,
    "baseline_2": baseline.mace_2,
}


def get_mace(mace_name, **options):
    """
    Retrieve a mace object by its name and initialize it with the given options.

    Args:
        mace_name (str): The name of the mace to retrieve.
        **options: Arbitrary keyword arguments to initialize the mace.

    Returns:
        object: An instance of the mace corresponding to the given name.

    Raises:
        KeyError: If the mace_name does not exist in the _maces dictionary.
    """
    return _maces[mace_name](**options)
