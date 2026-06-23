"""Baseline Wilson-action Metropolis run on a tiny SU(2) lattice."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rqm_yang_mills.lattice import Lattice4D
from rqm_yang_mills.monte_carlo import run_metropolis


def main() -> None:
    output_data = ROOT / "outputs" / "data"
    output_figures = ROOT / "outputs" / "figures"
    output_data.mkdir(parents=True, exist_ok=True)
    output_figures.mkdir(parents=True, exist_ok=True)

    lattice = Lattice4D((2, 2, 2, 2))
    _, records = run_metropolis(
        lattice,
        beta=2.2,
        n_sweeps=12,
        step_size=0.45,
        thermalization=0,
        measure_every=1,
        hot_start=False,
        seed=2002,
    )

    csv_path = output_data / "exp_002_wilson_action_metropolis.csv"
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["sweep", "action", "average_plaquette", "acceptance_rate"])
        writer.writeheader()
        writer.writerows(records)

    sweeps = [record["sweep"] for record in records]
    action = [record["action"] for record in records]
    average_plaquette = [record["average_plaquette"] for record in records]

    fig, axes = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
    axes[0].plot(sweeps, action, marker="o", linewidth=1.5)
    axes[0].set_ylabel("Wilson action")
    axes[1].plot(sweeps, average_plaquette, marker="o", color="tab:green", linewidth=1.5)
    axes[1].set_xlabel("sweep")
    axes[1].set_ylabel("average plaquette")
    fig.suptitle("Baseline SU(2) Wilson-action Metropolis")
    fig.tight_layout()
    fig.savefig(output_figures / "exp_002_wilson_action_metropolis.png", dpi=160)

    print(f"wrote {csv_path}")


if __name__ == "__main__":
    main()
