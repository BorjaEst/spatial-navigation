"""
Generate a random maps with a mace-like structure.
"""

import matplotlib.pyplot as plt
import torch

# pylint: disable=redefined-builtin
# pylint: disable=redefined-outer-name


def random(size, num_points):
    """
    Generate a random map with the given size and number of points.
    The points are evenly clustered to resemble a mace-like structure.
    """
    mace = torch.zeros(size, dtype=torch.bool)
    num_clusters = max(1, num_points // 10)  # Define the number of clusters
    cluster_radius = min(size) // 20  # Define a cluster radius based on the size

    # Generate evenly spaced cluster centers
    cluster_centers = []
    for _ in range(num_clusters):
        center_x = torch.randint(0, size[0], (1,))
        center_y = torch.randint(0, size[1], (1,))
        cluster_centers.append((center_x, center_y))

    for center_x, center_y in cluster_centers:
        # Generate points around each cluster center
        for _ in range(num_points // num_clusters):
            x = torch.clamp(center_x + torch.randint(-cluster_radius, cluster_radius + 1, (1,)), 0, size[0] - 1)
            y = torch.clamp(center_y + torch.randint(-cluster_radius, cluster_radius + 1, (1,)), 0, size[1] - 1)
            mace[x, y] = 1

    return mace


def free(mace):
    """Given a mace, return a random free point not colliding with the mace."""
    for _ in range(100):
        x = torch.randint(0, mace.shape[0], (1,))
        y = torch.randint(0, mace.shape[1], (1,))
        if mace[x, y] == 0:
            zeros = torch.zeros_like(mace, dtype=torch.bool)
            zeros[x, y] = 1
            return zeros
    raise ValueError("No free point found in the mace.")


def sensor(mace, position, decay=0.2):
    """
    Get the sensor readings from the mace at the agent's position.
    The `position` is a boolean tensor of the same shape as `mace`,
    where the agent's location (x, y) is marked as 1.

    The sensor readings are calculated based on a Gaussian decay from the agent's position.
    Walls (mace positions) have negative values, closer to -1 as they approach the agent's position.
    """
    # Find the agent's location
    agent_location = torch.nonzero(position, as_tuple=True)

    # Calculate distances from the agent's position using matrix operations
    x_indices = torch.arange(mace.shape[0], dtype=torch.float32).unsqueeze(1).repeat(1, mace.shape[1])
    y_indices = torch.arange(mace.shape[1], dtype=torch.float32).unsqueeze(0).repeat(mace.shape[0], 1)

    agent_x, agent_y = agent_location[0].item(), agent_location[1].item()
    distance_tensor = torch.sqrt((x_indices - agent_x) ** 2 + (y_indices - agent_y) ** 2)

    # Apply Gaussian decay to the distances
    gaussian_decay = torch.exp(-decay * distance_tensor)

    # Set walls (mace positions) to negative values based on Gaussian decay
    sensor_readings = gaussian_decay.clone()
    sensor_readings[mace] = -gaussian_decay[mace]

    return sensor_readings


def near(mace, position):
    """
    Determine the areas near the agent's position on the mace.
    The `position` is a boolean tensor of the same shape as `mace`,
    where the agent's location (x, y) is marked as 1.
    """
    # Ensure position is a boolean tensor
    assert position.shape == mace.shape, "Position must have the same shape as mace."

    # Find the agent's location
    agent_location = torch.nonzero(position, as_tuple=True)

    # Define a neighborhood around the agent (e.g., 1-cell radius)
    neighborhood = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx, ny = agent_location[0] + dx, agent_location[1] + dy
            if 0 <= nx < mace.shape[0] and 0 <= ny < mace.shape[1]:
                neighborhood.append((nx, ny))

    # Create a tensor marking the neighborhood
    near_tensor = torch.zeros_like(mace, dtype=torch.bool)
    for nx, ny in neighborhood:
        near_tensor[nx, ny] = True

    return near_tensor


def random_near(mace, position):
    """
    Randomly select a point near the agent's position on the mace.
    The `position` is a boolean tensor of the same shape as `mace`,
    where the agent's location (x, y) is marked as 1.
    """
    near_area = near(mace, position)
    near_indices = torch.nonzero(near_area, as_tuple=True)
    if len(near_indices[0]) == 0:
        raise ValueError("No free point found in the near area.")
    random_index = torch.randint(0, len(near_indices[0]), (1,))
    x, y = near_indices[0][random_index], near_indices[1][random_index]
    new_position = torch.zeros_like(mace, dtype=torch.bool)
    new_position[x, y] = 1
    return new_position


def plot(mace, position=None, near_area=None, ax=None):
    """
    Plot the given map with optional position and near area overlays.
    - `mace`: The mace map (2D tensor).
    - `position`: Optional boolean tensor marking the agent's position.
    - `near_area`: Optional boolean tensor marking the near area.
    - `ax`: Optional matplotlib axis for plotting.
    """
    if ax is None:
        _fig, ax = plt.subplots()

    # Create an RGB image for visualization
    display = torch.zeros((*mace.shape, 3), dtype=torch.float32)  # RGB image
    display[..., 0] = mace  # Red channel for walls

    if near_area is not None:
        display[..., 1] = near_area  # Green channel for near area

    if position is not None:
        display[..., 2] = position  # Blue channel for agent position

    ax.imshow(display.numpy(), interpolation="nearest")
    ax.axis("off")

    if ax is None:
        plt.show()


if __name__ == "__main__":
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    maces = [random(size=(40, 20), num_points=200) for _ in range(2)]

    for i, mace in enumerate(maces):
        agent_position = free(mace)  # Get a free position for the agent
        near_area = near(mace, agent_position)  # Get the near area around the agent

        # Combine mace, agent position, and near area for visualization
        plot(mace, position=agent_position, near_area=near_area, ax=ax[i])

    plt.show()
