import numpy as np
from src.modulation import calculate_insertion_indices
from src.voltage import calculate_stepped_phase_voltage


def calculate_three_phase_voltages(t, f_grid, modulation_index, vdc, number_of_submodules):
    phase_a = 0
    phase_b = -2 * np.pi / 3
    phase_c = 2 * np.pi / 3

    n_upper_a, n_lower_a = calculate_insertion_indices(t, f_grid, modulation_index, phase_a)
    n_upper_b, n_lower_b = calculate_insertion_indices(t, f_grid, modulation_index, phase_b)
    n_upper_c, n_lower_c = calculate_insertion_indices(t, f_grid, modulation_index, phase_c)

    v_a = calculate_stepped_phase_voltage(n_upper_a, n_lower_a, vdc, number_of_submodules)
    v_b = calculate_stepped_phase_voltage(n_upper_b, n_lower_b, vdc, number_of_submodules)
    v_c = calculate_stepped_phase_voltage(n_upper_c, n_lower_c, vdc, number_of_submodules)

    return v_a, v_b, v_c