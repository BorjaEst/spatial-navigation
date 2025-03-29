import matplotlib.pyplot as plt
import numpy as np


def raster(spikes, title, figsize=(12, 8), **kwds):
    """Plot the raster plot of the spikes."""
    num_time_steps, num_neurons = spikes.shape
    time_indices, neuron_indices = np.where(spikes == 1)

    plt.figure(figsize=figsize)
    plt.title(title)
    plt.plot(time_indices, neuron_indices, ".", **kwds)

    plt.ylabel("Neuron index")
    plt.yticks(np.linspace(0, num_neurons, min(11, num_neurons), dtype=int))

    plt.xlabel("Time step")
    plt.xlim(0, num_time_steps)

    plt.grid(axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


def signal(output, title, figsize=(12, 8), **kwds):
    """Plot the signal output."""
    num_time_steps, _num_neurons = output.shape
    time_steps = np.arange(num_time_steps)

    plt.figure(figsize=figsize)
    plt.title(title)
    plt.plot(time_steps, output, "--", **kwds)

    plt.ylabel("Firing Rate")
    plt.xlabel("Time")
    plt.show()
