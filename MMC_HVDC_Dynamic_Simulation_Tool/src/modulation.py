import numpy as np


def create_time_axis(sim_time, dt):
    return np.arange(0, sim_time, dt)


def calculate_insertion_indices(t, f_grid, modulation_index, phase_shift=0):
    omega = 2 * np.pi * f_grid

    n_upper = 0.5 * (1 - modulation_index * np.sin(omega * t + phase_shift))
    n_lower = 0.5 * (1 + modulation_index * np.sin(omega * t + phase_shift))

    return n_upper, n_lower