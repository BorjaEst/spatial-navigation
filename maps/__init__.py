"""
This module provides functionality to retrieve and initialize map objects.

Modules:
    maps.example: Contains example map definitions.

Functions:
    get_map(map_name, **options):
"""

from maps.example import example_map

_maps = {
    "example": example_map,
}


def get_map(map_name, **options):
    """
    Retrieve a map object by its name and initialize it with the given options.

    Args:
        map_name (str): The name of the map to retrieve.
        **options: Arbitrary keyword arguments to initialize the map.

    Returns:
        object: An instance of the map corresponding to the given name.

    Raises:
        KeyError: If the map_name does not exist in the _maps dictionary.
    """
    return _maps[map_name](**options)
