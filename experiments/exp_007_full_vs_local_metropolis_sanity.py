"""Compare full-action and local-action Metropolis paths on tiny lattices."""

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
from yang_mills_gap.monte_carlo import metropolis_sweep_full_action, metropolis_sweep_local
from yang_mills_gap.observables import average_closure_defect
from yang_mills_gap.wilson_action import wilson_action


def main() -> None:
    data_dir = ROOT / "outputs" / "data"
    fig_dir = ROOT / "outputs" / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    lattice = Lattice4D((2, 2, 2, 2))
    beta = 2.2
    n_sweeps = 6
    rng_start = np.random.default_rng(7007)
    initial = GaugeField.random(lattice, rng_start)
    full_field = initial.copy()
    local_field = initial.copy()
    full_rng = np.random.default_rng(7707)
    local_rng = np.random.default_rng(7707)

    records: list[dict[str, float]] = []
    for sweep in range(1, n_sweeps + 1):
        full_stats = metropolis_sweep_full_action(full_field, beta, step_size=0.35, rng=full_rng)
        local_stats = metropolis_sweep_local(local_field, beta, step_size=0.35, rng=local_rng)
        records.append(
            {
                "sweep": float(sweep),
                "full_action": wilson_action(full_field, beta),
                "local_action": wilson_action(local_field, beta),
                "action_abs_diff": abs(wilson_action(full_field, beta) - wilson_action(local_field, beta)),
                "full_average_closure_defect": average_closure_defect(full_field),
                "local_average_closure_defect": average_closure_defect(local_field),
                "closure_abs_diff": abs(average_closure_defect(full_field) - average_closure_defect(local_field)),
                "full_acceptance_rate": full_stats.acceptance_rate,
                "local_acceptance_rate": local_stats.acceptance_rate,
                "max_link_abs_diff": float(np.max(np.abs(full_field.links - local_field.links))),
            }
        )

    csv_path = data_dir / "exp_007_full_vs_local_metropolis_sanity.csv"
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)

    sweeps = [record["sweep"] for record in records]
    fig, axes = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
    axes[0].plot(sweeps, [record["full_action"] for record in records], marker="o", label="full action")
    axes[0].plot(sweeps, [record["local_action"] for record in records], marker="s", label="local action")
    axes[0].set_ylabel("Wilson action")
    axes[0].legend()
    axes[1].plot(sweeps, [record["action_abs_diff"] for record in records], marker="o")
    axes[1].set_xlabel("sweep")
    axes[1].set_ylabel("|delta action|")
    fig.suptitle("Full-action vs local-action Metropolis sanity check")
    fig.tight_layout()
    fig.savefig(fig_dir / "exp_007_full_vs_local_metropolis_sanity.png", dpi=160)


if __name__ == "__main__":
    main()
