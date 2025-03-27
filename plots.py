import matplotlib.pyplot as plt
import torch


def raster(spikes, title="Raster Plot"):
    """Plot the raster plot of the spikes."""
    plt.figure()
    for neuron_idx in range(spikes.shape[1]):
        spike_times = torch.nonzero(spikes[:, neuron_idx]).squeeze()
        plt.scatter(spike_times, neuron_idx * torch.ones_like(spike_times), s=1)
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Neuron Index")
    plt.xlim(0, spikes.shape[0])
    plt.ylim(0, spikes.shape[1])
    plt.show()


def signal(output, title="Firing Rates"):
    """Plot the signal output."""
    plt.figure()
    plt.plot(output)
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Firing Rate")
    plt.show()
