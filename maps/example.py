from ehc_sn.maps import Wall, Goal, Environment


@Environment(mission="grand mission").register_map
def example_map(env, grid, width, height):
    # Generate the surrounding walls
    grid.wall_rect(0, 0, width, height)

    # Generate vertical separation wall
    for i in range(0, height):
        grid.set(5, i, Wall())

    # Place a goal square in the bottom-right corner
    env.put_obj(Goal(), width - 2, height - 2)

    # Place the agent
    if env.agent_start_pos is not None:
        env.agent_pos = env.agent_start_pos
        env.agent_dir = env.agent_start_dir
    else:
        env.place_agent()

    env.mission = "grand mission"
