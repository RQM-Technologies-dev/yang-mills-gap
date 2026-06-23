"""Broad sanity comparison of full-action and local-action Metropolis sweeps.

The two chains intentionally use different random streams. This tiny
finite-lattice diagnostic checks that the local-action path lands in the same
rough observable range as the slower full-action reference path; it does not
require identical trajectories.
"""

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

    lattice = Lattice4D((2, 2, 2, 2))
    beta = 2.2
    common_kwargs = {
        "n_sweeps": 8,
        "step_size": 0.35,
        "thermalization": 0,
        "measure_every": 1,
        "hot_start": True,
    }
    _, full_records = run_metropolis(
        lattice,
        beta,
        use_local_action=False,
        seed=7007,
        **common_kwargs,
    )
    _, local_records = run_metropolis(
        lattice,
        beta,
        use_local_action=True,
        seed=8008,
        **common_kwargs,
    )

    rows: list[dict[str, float | str]] = []
    for kind, records in [("full_action", full_records), ("local_action", local_records)]:
        for record in records:
            rows.append(
                {
                    "kind": kind,
                    "sweep": record["sweep"],
                    "acceptance_rate": record["acceptance_rate"],
                    "average_plaquette": record["average_plaquette"],
                    "average_closure_defect": record["average_closure_defect"],
                    "action": record["action"],
                }
            )

    csv_path = data_dir / "exp_007_full_vs_local_metropolis_sanity.csv"
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "kind",
                "sweep",
                "acceptance_rate",
                "average_plaquette",
                "average_closure_defect",
                "action",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    sweeps = [record["sweep"] for record in full_records]
    fig, axes = plt.subplots(3, 1, figsize=(7, 8), sharex=True)
    for records, label in [(full_records, "full action"), (local_records, "local action")]:
        axes[0].plot(sweeps, [record["acceptance_rate"] for record in records], marker="o", label=label)
        axes[1].plot(sweeps, [record["average_plaquette"] for record in records], marker="o", label=label)
        axes[2].plot(sweeps, [record["average_closure_defect"] for record in records], marker="o", label=label)

    axes[0].set_ylabel("acceptance")
    axes[1].set_ylabel("avg plaquette")
    axes[2].set_ylabel("avg D_p")
    axes[2].set_xlabel("sweep")
    axes[0].legend()
    fig.suptitle("Full-action vs local-action tiny-lattice sanity diagnostic")
    fig.tight_layout()
    fig.savefig(fig_dir / "exp_007_full_vs_local_metropolis_sanity.png", dpi=160)


if __name__ == "__main__":
    main()
