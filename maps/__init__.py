from maps.example import example_map

_maps = {
    "example": example_map,
}


def get_map(map_name):
    """Return the map function for the given map name."""
    return _maps[map_name]
