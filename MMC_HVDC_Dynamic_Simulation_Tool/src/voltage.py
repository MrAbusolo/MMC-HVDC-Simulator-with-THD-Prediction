import numpy as np


def calculate_ideal_phase_voltage(n_upper, n_lower, vdc):
    v_upper = n_upper * vdc
    v_lower = n_lower * vdc

    return 0.5 * (v_lower - v_upper)


def calculate_stepped_phase_voltage(n_upper, n_lower, vdc, number_of_submodules):
    n_upper_steps = np.round(n_upper * number_of_submodules)
    n_lower_steps = np.round(n_lower * number_of_submodules)

    v_sm = vdc / number_of_submodules

    v_upper_stepped = n_upper_steps * v_sm
    v_lower_stepped = n_lower_steps * v_sm

    return 0.5 * (v_lower_stepped - v_upper_stepped)