"""
This module defines an example mace for a spatial navigation environment.
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


@Environment(defaults=Settings).mace_generator("mission example")
def mace_1(env, grid, width, height):

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


@Environment(defaults=Settings).mace_generator("mission example")
def mace_2(env, grid, width, height):

    # Generate the surrounding walls
    grid.wall_rect(0, 0, width, height)

    # Generate vertical separation wall
    for i in range(1, width - 2):
        grid.set(i, 3, Wall())

    # Place a goal square in the bottom-right corner
    env.put_obj(Goal(), width - 2, height - 2)

    # Place the agent
    env.agent_pos = (1, 1)
    env.agent_dir = 0
