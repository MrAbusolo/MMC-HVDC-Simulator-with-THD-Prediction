import os
import matplotlib.pyplot as plt
from src.voltage import calculate_stepped_phase_voltage


PLOT_DIR = "results/plots"


def save_and_show(filename):
    os.makedirs(PLOT_DIR, exist_ok=True)
    plt.savefig(os.path.join(PLOT_DIR, filename), dpi=300, bbox_inches="tight")
    plt.show()


def plot_insertion_indices(t, n_upper, n_lower):
    plt.figure()
    plt.plot(t, n_upper, label="Upper arm")
    plt.plot(t, n_lower, label="Lower arm")
    plt.xlabel("Time [s]")
    plt.ylabel("Insertion index")
    plt.title("MMC Insertion Indices")
    plt.legend()
    plt.grid(True)
    save_and_show("insertion_indices.png")


def plot_ideal_vs_stepped(t, v_phase, v_phase_stepped):
    plt.figure()
    plt.plot(t, v_phase, label="Ideal phase voltage")
    plt.plot(t, v_phase_stepped, label="Stepped phase voltage")
    plt.xlabel("Time [s]")
    plt.ylabel("Voltage [V]")
    plt.title("Ideal vs Stepped MMC Phase Voltage")
    plt.legend()
    plt.grid(True)
    save_and_show("ideal_vs_stepped_voltage.png")


def plot_submodule_comparison(t, n_upper, n_lower, vdc, n_values):
    plt.figure()

    for n in n_values:
        v_phase_stepped = calculate_stepped_phase_voltage(n_upper, n_lower, vdc, n)
        plt.plot(t, v_phase_stepped, label=f"N = {n}")

    plt.xlabel("Time [s]")
    plt.ylabel("Voltage [V]")
    plt.title("Effect of Submodule Number on MMC Output Voltage")
    plt.legend()
    plt.grid(True)
    save_and_show("submodule_comparison.png")


def plot_harmonic_spectrum(frequencies, magnitudes, max_frequency=2000):
    plt.figure(figsize=(12, 6))

    mask = frequencies <= max_frequency

    plt.stem(frequencies[mask], magnitudes[mask])
    plt.yscale("log")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Magnitude [V] - log scale")
    plt.title("Harmonic Spectrum of MMC Phase Voltage")
    plt.grid(True, which="both")
    save_and_show("harmonic_spectrum.png")


def plot_thd_vs_submodules(thd_results):
    n_values = list(thd_results.keys())
    thd_percent = [value * 100 for value in thd_results.values()]

    plt.figure()
    plt.plot(n_values, thd_percent, marker="o")
    plt.xlabel("Number of Submodules per Arm")
    plt.ylabel("THD [%]")
    plt.title("THD vs Number of Submodules")
    plt.grid(True)
    save_and_show("thd_vs_submodules.png")


def plot_three_phase_voltages(t, v_a, v_b, v_c):
    plt.figure()
    plt.plot(t, v_a, label="Phase A")
    plt.plot(t, v_b, label="Phase B")
    plt.plot(t, v_c, label="Phase C")
    plt.xlabel("Time [s]")
    plt.ylabel("Voltage [V]")
    plt.title("Three-Phase MMC Phase Voltages")
    plt.legend()
    plt.grid(True)
    save_and_show("three_phase_voltages.png")


def plot_line_voltages(t, v_ab, v_bc, v_ca):
    plt.figure()
    plt.plot(t, v_ab, label="Vab")
    plt.plot(t, v_bc, label="Vbc")
    plt.plot(t, v_ca, label="Vca")
    plt.xlabel("Time [s]")
    plt.ylabel("Voltage [V]")
    plt.title("Three-Phase MMC Line-to-Line Voltages")
    plt.legend()
    plt.grid(True)
    save_and_show("line_to_line_voltages.png")