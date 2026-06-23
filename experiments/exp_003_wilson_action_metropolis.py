"""Baseline Wilson-action Metropolis run."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from yang_mills_gap.lattice import Lattice4D
from yang_mills_gap.monte_carlo import run_metropolis


def main() -> None:
    data_dir = ROOT / "outputs" / "data"
    fig_dir = ROOT / "outputs" / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    _, records = run_metropolis(
        Lattice4D((2, 2, 2, 2)),
        beta=2.2,
        n_sweeps=12,
        step_size=0.45,
        seed=3003,
    )

    csv_path = data_dir / "exp_003_wilson_action_metropolis.csv"
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["sweep", "action", "average_plaquette", "average_closure_defect", "acceptance_rate"],
        )
        writer.writeheader()
        writer.writerows(records)

    sweeps = [record["sweep"] for record in records]
    fig, axes = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
    axes[0].plot(sweeps, [record["action"] for record in records], marker="o")
    axes[0].set_ylabel("Wilson action")
    axes[1].plot(sweeps, [record["average_closure_defect"] for record in records], marker="o", color="tab:green")
    axes[1].set_xlabel("sweep")
    axes[1].set_ylabel("avg D_p")
    fig.suptitle("Standard SU(2) Wilson-action Metropolis")
    fig.tight_layout()
    fig.savefig(fig_dir / "exp_003_wilson_action_metropolis.png", dpi=160)


if __name__ == "__main__":
    main()
