"""
This module defines an example map for a spatial navigation environment.
"""

import dataclasses as dc

from spnav.environment import BaseSettings, Environment, Goal, Wall


@dc.dataclass
class Settings(BaseSettings):
    """
    Settings class for configuring the spatial navigation environment.

    Attributes:
        grid_size (int): Size of the grid.
        max_steps (int): Maximum number of steps.
        see_through_walls (bool): Whether the agent can see through walls.
        agent_view_size (int): Size of the agent's view.
        render_mode (str): Default rendering mode (e.g., "human").
        screen_size (int): Size of the screen.
        highlight (bool): Whether to highlight the agent.
        agent_pov (bool): Whether to use the agent's point of view.
    """

    grid_size: int = 10  # size of the grid
    max_steps: int = 100  # maximum number of steps
    see_through_walls: bool = False  # whether the agent can see through
    agent_view_size: int = 7  # size of the agent's view
    render_mode: str = "human"  # default rendering mode as a humana
    screen_size: int = 640  # size of the screen
    highlight: bool = True  # whether to highlight the agent
    agent_pov: bool = False  # whether to use the agent's point of view


@Environment(defaults=Settings).map_generator("mission example")
def example_map(env, grid, width, height):
    """
    Sets up an example map in the given environment.

    Args:
        env: The environment object where the map will be set up.
        grid: The grid object representing the map layout.
        width: The width of the map.
        height: The height of the map.

    The function performs the following steps:
    1. Generates the surrounding walls of the map.
    2. Generates a vertical separation wall at x-coordinate 5.
    3. Places a goal square in the bottom-right corner of the map.
    4. Places the agent at the starting position (1, 1), direction 0.
    """

    # Generate the surrounding walls
    grid.wall_rect(0, 0, width, height)

    # Generate vertical separation wall
    for i in range(1, height - 2):
        grid.set(5, i, Wall())

    # Place a goal square in the bottom-right corner
    env.put_obj(Goal(), width - 2, height - 2)

    # Place the agent
    env.agent_pos = (1, 1)
    env.agent_dir = 0
