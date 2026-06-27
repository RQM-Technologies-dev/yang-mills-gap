"""Quarantined nonstandard anchor-deformation comparison.

This script changes the baseline action by adding a nonstandard anchor term.
It is not standard SU(2) Wilson lattice Yang-Mills and is not evidence for a
Clay-problem result. It is not part of the proof route.
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

from yang_mills_gap.gauge_field import GaugeField
from yang_mills_gap.lattice import Lattice4D
from yang_mills_gap.monte_carlo import propose_link, run_metropolis
from yang_mills_gap.observables import average_closure_defect
from yang_mills_gap.plaquette import all_closure_defects


def anchor_deformed_action(field: GaugeField, beta: float, anchor_strength: float, target_defect: float) -> float:
    defects = all_closure_defects(field)
    return float(beta * np.sum(defects) + anchor_strength * np.sum((defects - target_defect) ** 2))


def anchor_deformed_sweep(
    field: GaugeField,
    beta: float,
    anchor_strength: float,
    target_defect: float,
    step_size: float,
    rng: np.random.Generator,
) -> float:
    accepted = 0
    proposed = 0
    current_action = anchor_deformed_action(field, beta, anchor_strength, target_defect)
    for site in field.lattice.sites():
        for mu in range(4):
            old_link = field.link(site, mu).copy()
            field.set_link(site, mu, propose_link(old_link, step_size, rng))
            new_action = anchor_deformed_action(field, beta, anchor_strength, target_defect)
            delta = new_action - current_action
            proposed += 1
            if delta <= 0.0 or rng.random() < np.exp(-delta):
                accepted += 1
                current_action = new_action
            else:
                field.set_link(site, mu, old_link)
    return accepted / proposed


def main() -> None:
    data_dir = ROOT / "outputs" / "data"
    fig_dir = ROOT / "outputs" / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    lattice = Lattice4D((2, 2, 2, 2))
    beta = 2.2
    anchor_strength = 0.8
    target_defect = 0.35
    rng = np.random.default_rng(6006)
    _, standard_records = run_metropolis(lattice, beta, n_sweeps=8, step_size=0.40, seed=6006)

    deformed_field = GaugeField.cold(lattice)
    deformed_records: list[dict[str, float]] = []
    for sweep in range(1, 9):
        acceptance = anchor_deformed_sweep(
            deformed_field,
            beta,
            anchor_strength,
            target_defect,
            step_size=0.40,
            rng=rng,
        )
        deformed_records.append(
            {
                "sweep": float(sweep),
                "mean_closure_defect": average_closure_defect(deformed_field),
                "acceptance_rate": acceptance,
            }
        )

    csv_path = data_dir / "exp_006_rqm_anchor_deformation_nonstandard.csv"
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["kind", "sweep", "mean_closure_defect", "acceptance_rate"])
        writer.writeheader()
        for record in standard_records:
            writer.writerow(
                {
                    "kind": "standard_wilson",
                    "sweep": record["sweep"],
                    "mean_closure_defect": record["average_closure_defect"],
                    "acceptance_rate": record["acceptance_rate"],
                }
            )
        for record in deformed_records:
            writer.writerow({"kind": "anchor_deformed_nonstandard", **record})

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(
        [record["sweep"] for record in standard_records],
        [record["average_closure_defect"] for record in standard_records],
        marker="o",
        label="standard Wilson",
    )
    ax.plot(
        [record["sweep"] for record in deformed_records],
        [record["mean_closure_defect"] for record in deformed_records],
        marker="s",
        label="nonstandard anchor deformation",
    )
    ax.axhline(target_defect, color="black", linestyle="--", linewidth=1.0, label="anchor target")
    ax.set_xlabel("sweep")
    ax.set_ylabel("mean D_p")
    ax.set_title("Nonstandard anchor-deformation comparison")
    ax.legend()
    fig.tight_layout()
    fig.savefig(fig_dir / "exp_006_rqm_anchor_deformation_nonstandard.png", dpi=160)


if __name__ == "__main__":
    main()
