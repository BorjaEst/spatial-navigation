import matplotlib.pyplot as plt
import numpy as np


def raster(spikes, figsize=(12, 4), **kwds):
    """Plot the raster plot of the spikes."""
    num_time_steps, num_neurons = spikes.shape
    time_indices, neuron_indices = np.where(spikes == 1)

    plt.figure(figsize=figsize)
    plt.plot(time_indices, neuron_indices, ".", **kwds)

    plt.ylabel("Neuron index")
    plt.yticks(np.linspace(0, num_neurons, min(11, num_neurons), dtype=int))
    plt.ylim(0, num_neurons)

    plt.xlabel("Time step")
    plt.xlim(0, num_time_steps)

    plt.grid(axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout()


def signal(output, figsize=(12, 4), **kwds):
    """Plot the signal output."""
    num_time_steps, _num_neurons = output.shape
    time_steps = np.arange(num_time_steps)

    plt.figure(figsize=figsize)
    plt.plot(time_steps, output, "--", **kwds)

    plt.ylabel("Firing Rate")
    plt.xlabel("Time")
    plt.xlim(0, num_time_steps)

    plt.grid(axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout()


def weights(weights, figsize=(12, 4), **kwds):
    """Plot the weights."""

    plt.figure(figsize=figsize)
    plt.hist(weights.flatten(), 50, **kwds)

    plt.ylabel("Weight")
    plt.xlabel("Weight Value")

    plt.tight_layout()
