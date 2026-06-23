"""Nonstandard RQM-inspired anchor-deformation toy experiment.

This script intentionally does not belong to the baseline Yang-Mills
implementation. It adds an exploratory penalty to the plaquette closure defect
for comparison plots only. It must not be read as a Clay mass-gap proof or as a
standard lattice Yang-Mills action.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rqm_yang_mills.gauge_field import GaugeField
from rqm_yang_mills.lattice import Lattice4D
from rqm_yang_mills.monte_carlo import propose_link, run_metropolis
from rqm_yang_mills.plaquette import all_closure_defects
from rqm_yang_mills.wilson_action import wilson_action


def anchor_deformed_action(
    field: GaugeField,
    beta: float,
    *,
    anchor_strength: float,
    target_defect: float,
) -> float:
    defects = all_closure_defects(field)
    return float(beta * np.sum(defects) + anchor_strength * np.sum((defects - target_defect) ** 2))


def anchor_deformed_sweep(
    field: GaugeField,
    beta: float,
    *,
    anchor_strength: float,
    target_defect: float,
    step_size: float,
    rng: np.random.Generator,
) -> float:
    accepted = 0
    proposed = 0
    current_action = anchor_deformed_action(
        field,
        beta,
        anchor_strength=anchor_strength,
        target_defect=target_defect,
    )
    for site in field.lattice.sites():
        for mu in range(4):
            old_link = field.link(site, mu).copy()
            field.set_link(site, mu, propose_link(old_link, step_size, rng))
            new_action = anchor_deformed_action(
                field,
                beta,
                anchor_strength=anchor_strength,
                target_defect=target_defect,
            )
            delta = new_action - current_action
            proposed += 1
            if delta <= 0.0 or rng.random() < np.exp(-delta):
                accepted += 1
                current_action = new_action
            else:
                field.set_link(site, mu, old_link)
    return accepted / proposed


def main() -> None:
    output_data = ROOT / "outputs" / "data"
    output_figures = ROOT / "outputs" / "figures"
    output_data.mkdir(parents=True, exist_ok=True)
    output_figures.mkdir(parents=True, exist_ok=True)

    lattice = Lattice4D((2, 2, 2, 2))
    beta = 2.2
    anchor_strength = 0.8
    target_defect = 0.35
    rng = np.random.default_rng(6006)

    standard_field, standard_records = run_metropolis(
        lattice,
        beta,
        n_sweeps=8,
        step_size=0.40,
        hot_start=False,
        seed=6006,
    )

    deformed_field = GaugeField.cold(lattice)
    deformed_records: list[dict[str, float]] = []
    for sweep in range(1, 9):
        acceptance = anchor_deformed_sweep(
            deformed_field,
            beta,
            anchor_strength=anchor_strength,
            target_defect=target_defect,
            step_size=0.40,
            rng=rng,
        )
        defects = all_closure_defects(deformed_field)
        deformed_records.append(
            {
                "sweep": float(sweep),
                "action": anchor_deformed_action(
                    deformed_field,
                    beta,
                    anchor_strength=anchor_strength,
                    target_defect=target_defect,
                ),
                "mean_closure_defect": float(np.mean(defects)),
                "acceptance_rate": acceptance,
            }
        )

    csv_path = output_data / "exp_006_rqm_anchor_deformation.csv"
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "kind",
                "sweep",
                "action",
                "mean_closure_defect",
                "average_plaquette",
                "acceptance_rate",
            ],
        )
        writer.writeheader()
        for record in standard_records:
            writer.writerow(
                {
                    "kind": "standard_wilson",
                    "sweep": record["sweep"],
                    "action": record["action"],
                    "mean_closure_defect": 1.0 - record["average_plaquette"],
                    "average_plaquette": record["average_plaquette"],
                    "acceptance_rate": record["acceptance_rate"],
                }
            )
        for record in deformed_records:
            writer.writerow(
                {
                    "kind": "rqm_anchor_deformed_nonstandard",
                    "sweep": record["sweep"],
                    "action": record["action"],
                    "mean_closure_defect": record["mean_closure_defect"],
                    "average_plaquette": "",
                    "acceptance_rate": record["acceptance_rate"],
                }
            )

    standard_defects = all_closure_defects(standard_field).ravel()
    deformed_defects = all_closure_defects(deformed_field).ravel()

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(
        [record["sweep"] for record in standard_records],
        [1.0 - record["average_plaquette"] for record in standard_records],
        marker="o",
        label="standard Wilson",
    )
    axes[0].plot(
        [record["sweep"] for record in deformed_records],
        [record["mean_closure_defect"] for record in deformed_records],
        marker="s",
        label="anchor-deformed",
    )
    axes[0].axhline(target_defect, color="black", linestyle="--", linewidth=1.0, label="anchor target")
    axes[0].set_xlabel("sweep")
    axes[0].set_ylabel("mean D_p")
    axes[0].legend()

    bins = np.linspace(0.0, 1.2, 24)
    axes[1].hist(standard_defects, bins=bins, alpha=0.6, label="standard Wilson")
    axes[1].hist(deformed_defects, bins=bins, alpha=0.6, label="anchor-deformed")
    axes[1].set_xlabel("closure defect D_p")
    axes[1].set_ylabel("count")
    axes[1].legend()
    fig.suptitle("Nonstandard RQM anchor-deformation comparison")
    fig.tight_layout()
    fig.savefig(output_figures / "exp_006_rqm_anchor_deformation.png", dpi=160)

    print("Nonstandard anchor-deformed action used only in this experiment.")
    print(f"standard final action: {wilson_action(standard_field, beta):.6f}")
    print(f"deformed final action: {anchor_deformed_action(deformed_field, beta, anchor_strength=anchor_strength, target_defect=target_defect):.6f}")


if __name__ == "__main__":
    main()
