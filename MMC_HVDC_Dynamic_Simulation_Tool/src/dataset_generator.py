import os
import csv

from src.parameters import VDC, F_GRID, SIM_TIME, DT
from src.modulation import create_time_axis, calculate_insertion_indices
from src.voltage import calculate_stepped_phase_voltage
from src.harmonics import calculate_thd


def generate_thd_dataset(
    n_values,
    modulation_values,
    output_path="results/dataset.csv"
):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    t = create_time_axis(SIM_TIME, DT)

    rows = []

    for n in n_values:
        for m in modulation_values:
            n_upper, n_lower = calculate_insertion_indices(t, F_GRID, m)

            v_phase_stepped = calculate_stepped_phase_voltage(
                n_upper,
                n_lower,
                VDC,
                n
            )

            thd = calculate_thd(
                v_phase_stepped,
                DT,
                fundamental_frequency=F_GRID
            )

            rows.append({
                "N": n,
                "modulation_index": m,
                "THD": thd,
                "THD_percent": thd * 100
            })

    with open(output_path, mode="w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["N", "modulation_index", "THD", "THD_percent"]
        )

        writer.writeheader()
        writer.writerows(rows)

    return rows