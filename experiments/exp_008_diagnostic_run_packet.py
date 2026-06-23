"""Create a tiny finite-lattice diagnostic run packet.

This baseline Wilson-action packet is a reproducibility and diagnostics check,
not a mass-gap estimate.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from yang_mills_gap.experiment_driver import run_chain
from yang_mills_gap.run_packet import create_run_dir, save_diagnostics_json, save_figure, save_records_csv


def plot_series(values: list[float], running_values: list[float], ylabel: str, title: str):
    x = np.arange(len(values))
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(x, values, marker="o", linewidth=1.0, label=ylabel)
    ax.plot(x, running_values, linewidth=1.8, label="running mean")
    ax.set_xlabel("measurement")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    return fig


def plot_autocorrelation(values: list[float], ylabel: str, title: str):
    x = np.arange(len(values))
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.axhline(0.0, color="black", linewidth=0.8)
    ax.plot(x, values, marker="o", linewidth=1.2)
    ax.set_xlabel("lag")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    fig.tight_layout()
    return fig


def plot_thermalization_summary(windows: list[dict[str, float]], ylabel: str, title: str):
    cuts = [row["cut_fraction"] for row in windows]
    means = [row["mean"] for row in windows]
    stderr = [row["stderr"] for row in windows]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.errorbar(cuts, means, yerr=stderr, marker="o", capsize=3)
    ax.set_xlabel("discarded fraction")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    fig.tight_layout()
    return fig


def main() -> None:
    config = {
        "label": "tiny finite-lattice sanity diagnostic",
        "lattice_shape": (2, 2, 2, 2),
        "beta": 2.2,
        "n_sweeps": 16,
        "step_size": 0.35,
        "thermalization": 2,
        "measure_every": 1,
        "hot_start": True,
        "use_local_action": True,
        "seed": 8008,
        "claim_boundary": "diagnostic packet only; not a mass-gap estimate",
    }
    run_dir = create_run_dir(ROOT / "outputs" / "run_packets", "exp_008_diagnostic_run_packet", config)
    result = run_chain(
        lattice_shape=tuple(config["lattice_shape"]),
        beta=float(config["beta"]),
        n_sweeps=int(config["n_sweeps"]),
        step_size=float(config["step_size"]),
        thermalization=int(config["thermalization"]),
        measure_every=int(config["measure_every"]),
        hot_start=bool(config["hot_start"]),
        use_local_action=bool(config["use_local_action"]),
        seed=int(config["seed"]),
    )
    records = result["records"]
    diagnostics = result["diagnostics"]

    save_records_csv(run_dir / "observables.csv", records)
    save_diagnostics_json(run_dir / "diagnostics.json", diagnostics)

    action = [record["action"] for record in records]
    closure = [record["average_closure_defect"] for record in records]
    plots = [
        (
            plot_series(
                action,
                diagnostics["action"]["running_mean"],
                "action",
                "Action running mean",
            ),
            "action_running_mean.png",
        ),
        (
            plot_series(
                closure,
                diagnostics["average_closure_defect"]["running_mean"],
                "average D_p",
                "Closure-defect running mean",
            ),
            "closure_running_mean.png",
        ),
        (
            plot_autocorrelation(
                diagnostics["action"]["autocorrelation"],
                "rho_action(lag)",
                "Action autocorrelation",
            ),
            "action_autocorrelation.png",
        ),
        (
            plot_autocorrelation(
                diagnostics["average_closure_defect"]["autocorrelation"],
                "rho_closure(lag)",
                "Closure-defect autocorrelation",
            ),
            "closure_autocorrelation.png",
        ),
        (
            plot_thermalization_summary(
                diagnostics["action"]["thermalization_windows"],
                "action",
                "Action thermalization windows",
            ),
            "action_thermalization_windows.png",
        ),
        (
            plot_thermalization_summary(
                diagnostics["average_closure_defect"]["thermalization_windows"],
                "average D_p",
                "Closure-defect thermalization windows",
            ),
            "closure_thermalization_windows.png",
        ),
    ]
    for fig, filename in plots:
        save_figure(run_dir, fig, filename)
        plt.close(fig)

    print(f"Wrote diagnostic run packet: {run_dir}")


if __name__ == "__main__":
    main()
