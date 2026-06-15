import sys
import os

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.append(project_root)


from src.parameters import (
    VDC,
    F_GRID,
    MODULATION_INDEX,
    SIM_TIME,
    DT,
    DEFAULT_SUBMODULES
)

from src.modulation import (
    create_time_axis,
    calculate_insertion_indices
)

from src.voltage import (
    calculate_ideal_phase_voltage,
    calculate_stepped_phase_voltage
)

from src.harmonics import (
    calculate_fft,
    calculate_thd,
    print_largest_harmonics,
    calculate_thd_for_multiple_submodules
)

from src.three_phase import (
    calculate_three_phase_voltages
)

from src.power_system import (
    calculate_line_voltages
)

from src.plotting import (
    plot_insertion_indices,
    plot_ideal_vs_stepped,
    plot_submodule_comparison,
    plot_harmonic_spectrum,
    plot_thd_vs_submodules,
    plot_three_phase_voltages,
    plot_line_voltages
)

from src.dataset_generator import (
    generate_thd_dataset
)

from src.ml_models import (
    train_linear_regression,
    train_neural_network
)


print("Program started")

t = create_time_axis(SIM_TIME, DT)

n_upper, n_lower = calculate_insertion_indices(
    t,
    F_GRID,
    MODULATION_INDEX
)

v_phase = calculate_ideal_phase_voltage(
    n_upper,
    n_lower,
    VDC
)

v_phase_stepped = calculate_stepped_phase_voltage(
    n_upper,
    n_lower,
    VDC,
    DEFAULT_SUBMODULES
)

frequencies, magnitudes = calculate_fft(
    v_phase_stepped,
    DT
)

print_largest_harmonics(
    frequencies,
    magnitudes
)

thd = calculate_thd(
    v_phase_stepped,
    DT,
    fundamental_frequency=F_GRID
)

print(f"\nTHD for N = {DEFAULT_SUBMODULES}: {thd * 100:.2f}%")

plot_insertion_indices(
    t,
    n_upper,
    n_lower
)

plot_ideal_vs_stepped(
    t,
    v_phase,
    v_phase_stepped
)

plot_submodule_comparison(
    t,
    n_upper,
    n_lower,
    VDC,
    n_values=[5, 10, 20, 50]
)

plot_harmonic_spectrum(
    frequencies,
    magnitudes
)

thd_results = calculate_thd_for_multiple_submodules(
    n_upper,
    n_lower,
    VDC,
    DT,
    n_values=[5, 10, 20, 50, 100],
    fundamental_frequency=F_GRID
)

print("\nTHD vs Submodule Number")
print("----------------------")

for n, thd_value in thd_results.items():
    print(f"N = {n:3d}    THD = {thd_value * 100:.2f}%")

plot_thd_vs_submodules(
    thd_results
)

v_a, v_b, v_c = calculate_three_phase_voltages(
    t,
    F_GRID,
    MODULATION_INDEX,
    VDC,
    DEFAULT_SUBMODULES
)

v_ab, v_bc, v_ca = calculate_line_voltages(
    v_a,
    v_b,
    v_c
)

plot_three_phase_voltages(
    t,
    v_a,
    v_b,
    v_c
)

plot_line_voltages(
    t,
    v_ab,
    v_bc,
    v_ca
)

dataset = generate_thd_dataset(
    n_values=[5, 10, 20, 50, 100],
    modulation_values=[0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    output_path="results/dataset.csv"
)

print(f"\nDataset generated with {len(dataset)} rows.")
print("Saved to results/dataset.csv")

linear_model, linear_mae, linear_r2 = train_linear_regression(
    "results/dataset.csv"
)

neural_model, neural_mae, neural_r2 = train_neural_network(
    "results/dataset.csv"
)

print("\nMachine Learning Model Comparison")
print("---------------------------------")
print(f"Linear Regression MAE: {linear_mae:.4f}%")
print(f"Linear Regression R²:  {linear_r2:.4f}")
print()
print(f"Neural Network MAE:    {neural_mae:.4f}%")
print(f"Neural Network R²:     {neural_r2:.4f}")

prediction_input = [[30, 0.85]]

linear_prediction = linear_model.predict(
    prediction_input
)

neural_prediction = neural_model.predict(
    prediction_input
)

print("\nPrediction Example")
print("------------------")
print("Input: N = 30, modulation index = 0.85")
print(f"Linear Regression predicted THD: {linear_prediction[0]:.2f}%")
print(f"Neural Network predicted THD:    {neural_prediction[0]:.2f}%")

print("Program finished")