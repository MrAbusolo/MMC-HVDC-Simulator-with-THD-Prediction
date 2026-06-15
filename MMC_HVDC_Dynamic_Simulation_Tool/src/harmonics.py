import numpy as np
from src.voltage import calculate_stepped_phase_voltage


def calculate_fft(signal, dt):
    number_of_samples = len(signal)

    frequencies = np.fft.rfftfreq(number_of_samples, dt)
    fft_values = np.fft.rfft(signal)

    magnitudes = np.abs(fft_values) / number_of_samples
    magnitudes[1:] = 2 * magnitudes[1:]

    return frequencies, magnitudes


def calculate_thd(signal, dt, fundamental_frequency=50, max_harmonic_order=40):
    frequencies, magnitudes = calculate_fft(signal, dt)

    fundamental_index = np.argmin(np.abs(frequencies - fundamental_frequency))
    fundamental_magnitude = magnitudes[fundamental_index]

    harmonic_magnitudes = []

    for harmonic_order in range(2, max_harmonic_order + 1):
        harmonic_frequency = harmonic_order * fundamental_frequency
        harmonic_index = np.argmin(np.abs(frequencies - harmonic_frequency))
        harmonic_magnitudes.append(magnitudes[harmonic_index])

    harmonic_rms_sum = np.sqrt(np.sum(np.array(harmonic_magnitudes) ** 2))

    return harmonic_rms_sum / fundamental_magnitude


def calculate_thd_for_multiple_submodules(
    n_upper,
    n_lower,
    vdc,
    dt,
    n_values,
    fundamental_frequency=50
):
    thd_results = {}

    for n in n_values:
        v_phase_stepped = calculate_stepped_phase_voltage(n_upper, n_lower, vdc, n)
        thd = calculate_thd(v_phase_stepped, dt, fundamental_frequency)
        thd_results[n] = thd

    return thd_results


def print_largest_harmonics(frequencies, magnitudes, count=20):
    indices = np.argsort(magnitudes)[::-1]

    print("\nLargest Harmonics:")
    print("------------------")

    for i in range(count):
        idx = indices[i]
        print(f"f = {frequencies[idx]:8.2f} Hz    magnitude = {magnitudes[idx]:10.2f}")