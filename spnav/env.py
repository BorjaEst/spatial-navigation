"""
This module defines the `Environment` class and related components for
creating and managing grid-based environments using the MiniGrid framework.
"""

from abc import ABC
from typing import Literal, Optional, Tuple, TypeAlias

import numpy as np
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Goal, Wall
from minigrid.minigrid_env import MiniGridEnv
from pydantic import Field, PositiveInt
from pydantic_settings import BaseSettings

# Type aliases
Location: TypeAlias = Tuple[int, int]


class ExperimentSettings(BaseSettings):
    """Defines the configuration settings for the environment."""

    grid_size: Optional[PositiveInt] = Field(None, ge=1, le=20)
    width: Optional[PositiveInt] = Field(None, ge=1, le=20)
    height: Optional[PositiveInt] = Field(None, ge=1, le=20)
    max_steps: Optional[PositiveInt] = Field(None, ge=1)
    see_through_walls: bool = False
    agent_view_size: Optional[PositiveInt] = Field(6, ge=1, le=20)
    render_mode: Optional[str] = Field(None)
    screen_size: Optional[int] = Field(None, ge=640, le=1000)
    highlight: bool = True
    agent_pov: bool = False


class BlockSettings(ExperimentSettings):
    """Defines the configuration settings for the block environment."""

    name: str = Field()
    trajectories: PositiveInt = Field(5, ge=1)
    walls: list[Location | Literal["random"]] = Field([])
    goals: list[Location | Literal["random"]] = Field(["random"])
    start: Location | Literal["random"] = Field("random")


class LoggerEnv(MiniGridEnv, ABC):
    """Represent an environment that logs agent trajectories."""

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.trajectories = []  # Collect all trajectories
        self.observations = None

    def step(self, action):
        result = obs, reward, _, _, info = super().step(action)
        # _, _, _ = self.grid.encode().swapaxes(0, -1)  # Grid info
        self.observations.append(self.observation)
        return result

    def reset(self, **kwds):
        if self.observations is not None:
            observations_arr = np.array(self.observations)
            self.trajectories.append(observations_arr)
        self.observations = []
        return super().reset(**kwds)

    @property
    def observation(self):
        """Return the observation of the agent."""
        width, height = self.grid.width, self.grid.height
        observation = np.zeros((width, height), dtype=np.uint8)
        observation[*self.agent_pos] = 1
        return observation


class Mace(LoggerEnv, MiniGridEnv):
    """Represent an environment for spatial navigation."""

    def __init__(self, settings: BlockSettings):
        mission_space = MissionSpace(mission_func=self._mission)
        super().__init__(mission_space, **settings.model_dump())
        self.mission_name: str = settings.name
        self.walls = settings.walls
        self.goal_locations = settings.goals
        self.agent_start_pos = settings.start

    @staticmethod
    def _mission():
        return "Find the goal."

    def _gen_grid(self, width, height):
        self.grid = Grid(width, height)  # Create a grid
        self.gen_walls()  # Generate walls
        self.gen_goals()  # Generate goals
        self.gen_agent()  # Generate agent

    def gen_walls(self):
        """Generate walls in the grid."""
        for x, y in self.walls:
            self.grid.set(x, y, Wall())

    def gen_goals(self):
        """Generate goals in the grid."""
        for goal in self.goal_locations:
            if goal == "random":
                self.place_obj(Goal())
            else:
                self.put_obj(Goal(), *goal)

    def gen_agent(self):
        """Generate the agent in the grid."""
        if self.agent_start_pos == "random":
            self.place_agent()
        else:
            self.agent_pos = self.agent_start_pos

    def run(self, control, seed=42):
        """Run the environment for a number of steps."""
        for _ in range(self.trajectories):
            control(self, seed=seed).start()
        self.close()
        return self.trajectories
