"""Create a tiny correlator/effective-mass diagnostic run packet.

This baseline Wilson-action packet is diagnostic only. It is not a Clay
mass-gap result and does not use the nonstandard RQM anchor deformation.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from yang_mills_gap.correlators import bootstrap_correlator, temporal_correlator
from yang_mills_gap.diagnostics import autocorrelation, integrated_autocorrelation_time, running_mean, thermalization_window_summary
from yang_mills_gap.effective_mass import effective_mass, effective_mass_cosh
from yang_mills_gap.gauge_field import GaugeField
from yang_mills_gap.lattice import Lattice4D
from yang_mills_gap.monte_carlo import metropolis_sweep_local
from yang_mills_gap.observables import average_closure_defect, average_plaquette, glueball_timeseries
from yang_mills_gap.run_packet import (
    create_run_dir,
    save_array,
    save_config_json,
    save_diagnostics_json,
    save_figure,
    save_manifest_json,
    save_records_csv,
)
from yang_mills_gap.wilson_action import wilson_action


def compute_correlator_artifacts(
    samples: np.ndarray,
    *,
    n_bootstrap: int = 100,
    seed: int | None = None,
) -> dict[str, np.ndarray]:
    """Compute correlator and effective-mass arrays from glueball samples."""

    correlator = temporal_correlator(samples, connected=True)
    _, correlator_stderr, _ = bootstrap_correlator(
        samples,
        n_bootstrap=n_bootstrap,
        connected=True,
        seed=seed,
    )
    mass_log = effective_mass(correlator)
    mass_cosh = effective_mass_cosh(correlator)
    return {
        "correlator": correlator,
        "correlator_stderr": correlator_stderr,
        "effective_mass_log": mass_log,
        "effective_mass_cosh": mass_cosh,
    }


def series_diagnostics(values: np.ndarray) -> dict[str, Any]:
    max_lag = min(10, values.size - 1)
    return {
        "running_mean": running_mean(values).tolist(),
        "autocorrelation": autocorrelation(values, max_lag=max_lag).tolist(),
        "integrated_autocorrelation_time": integrated_autocorrelation_time(values),
        "thermalization_windows": thermalization_window_summary(values),
    }


def plot_running_mean(values: list[float], running_values: list[float], ylabel: str, title: str):
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


def plot_thermalization(windows: list[dict[str, float]], ylabel: str, title: str):
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


def plot_correlator(correlator: np.ndarray, stderr: np.ndarray):
    x = np.arange(correlator.size)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.errorbar(x, correlator, yerr=stderr, marker="o", capsize=3)
    ax.axhline(0.0, color="black", linewidth=0.8)
    ax.set_xlabel("temporal separation")
    ax.set_ylabel("connected C(t)")
    ax.set_title("Glueball-like correlator diagnostic")
    fig.tight_layout()
    return fig


def plot_effective_mass(mass_log: np.ndarray, mass_cosh: np.ndarray):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(np.arange(mass_log.size), mass_log, marker="o", label="log")
    ax.plot(np.arange(mass_cosh.size), mass_cosh, marker="s", label="cosh")
    ax.set_xlabel("t")
    ax.set_ylabel("m_eff(t)")
    ax.set_title("Effective-mass diagnostic")
    ax.legend()
    fig.tight_layout()
    return fig


def main() -> None:
    config = {
        "label": "tiny finite-lattice correlator/effective-mass sanity diagnostic",
        "lattice_shape": (1, 1, 1, 4),
        "beta": 2.2,
        "n_sweeps": 18,
        "step_size": 0.42,
        "thermalization": 4,
        "measure_every": 1,
        "hot_start": False,
        "use_local_action": True,
        "seed": 9009,
        "n_bootstrap": 100,
        "claim_boundary": "diagnostic packet only; not a mass-gap estimate",
    }
    run_dir = create_run_dir(ROOT / "outputs" / "run_packets", "exp_009_correlator_run_packet", config)
    save_config_json(run_dir / "config.json", config)

    rng = np.random.default_rng(int(config["seed"]))
    lattice = Lattice4D(tuple(config["lattice_shape"]))
    field = GaugeField.random(lattice, rng) if config["hot_start"] else GaugeField.cold(lattice)
    records: list[dict[str, float]] = []
    samples: list[np.ndarray] = []
    for sweep in range(1, int(config["n_sweeps"]) + 1):
        stats = metropolis_sweep_local(field, float(config["beta"]), step_size=float(config["step_size"]), rng=rng)
        if sweep > int(config["thermalization"]) and (sweep - int(config["thermalization"])) % int(config["measure_every"]) == 0:
            records.append(
                {
                    "sweep": float(sweep),
                    "action": wilson_action(field, float(config["beta"])),
                    "average_plaquette": average_plaquette(field),
                    "average_closure_defect": average_closure_defect(field),
                    "acceptance_rate": stats.acceptance_rate,
                }
            )
            samples.append(glueball_timeseries(field))

    sample_array = np.vstack(samples)
    artifacts = compute_correlator_artifacts(
        sample_array,
        n_bootstrap=int(config["n_bootstrap"]),
        seed=int(config["seed"]) + 1,
    )
    action = np.array([record["action"] for record in records], dtype=float)
    closure = np.array([record["average_closure_defect"] for record in records], dtype=float)
    diagnostics = {
        "action": series_diagnostics(action),
        "average_closure_defect": series_diagnostics(closure),
        "correlator": {
            "n_samples": float(sample_array.shape[0]),
            "nt": float(sample_array.shape[1]),
            "bootstrap_stderr_mean": float(np.mean(artifacts["correlator_stderr"])),
        },
        "summary": {
            "n_measurements": float(len(records)),
            "mean_acceptance_rate": float(np.mean([record["acceptance_rate"] for record in records])),
            "claim_boundary": config["claim_boundary"],
        },
    }

    save_records_csv(run_dir / "observables.csv", records)
    save_diagnostics_json(run_dir / "diagnostics.json", diagnostics)
    save_array(run_dir / "glueball_samples.npy", sample_array)
    save_records_csv(
        run_dir / "correlator.csv",
        [
            {
                "t": float(index),
                "connected_correlator": float(artifacts["correlator"][index]),
                "bootstrap_stderr": float(artifacts["correlator_stderr"][index]),
            }
            for index in range(artifacts["correlator"].size)
        ],
    )
    mass_log = artifacts["effective_mass_log"]
    mass_cosh = artifacts["effective_mass_cosh"]
    save_records_csv(
        run_dir / "effective_mass.csv",
        [
            {
                "t": float(index),
                "m_eff_log": float(mass_log[index]) if index < mass_log.size else "",
                "m_eff_cosh": float(mass_cosh[index]),
            }
            for index in range(mass_cosh.size)
        ],
    )

    plot_specs = [
        (plot_running_mean(action.tolist(), diagnostics["action"]["running_mean"], "action", "Action running mean"), "action_running_mean.png"),
        (
            plot_running_mean(
                closure.tolist(),
                diagnostics["average_closure_defect"]["running_mean"],
                "average D_p",
                "Closure-defect running mean",
            ),
            "closure_running_mean.png",
        ),
        (plot_autocorrelation(diagnostics["action"]["autocorrelation"], "rho_action(lag)", "Action autocorrelation"), "action_autocorrelation.png"),
        (
            plot_autocorrelation(
                diagnostics["average_closure_defect"]["autocorrelation"],
                "rho_closure(lag)",
                "Closure-defect autocorrelation",
            ),
            "closure_autocorrelation.png",
        ),
        (plot_thermalization(diagnostics["action"]["thermalization_windows"], "action", "Action thermalization windows"), "action_thermalization_windows.png"),
        (
            plot_thermalization(
                diagnostics["average_closure_defect"]["thermalization_windows"],
                "average D_p",
                "Closure-defect thermalization windows",
            ),
            "closure_thermalization_windows.png",
        ),
        (plot_correlator(artifacts["correlator"], artifacts["correlator_stderr"]), "correlator.png"),
        (plot_effective_mass(mass_log, mass_cosh), "effective_mass.png"),
    ]
    plot_manifest: dict[str, str] = {}
    for fig, filename in plot_specs:
        path = save_figure(run_dir, fig, filename)
        plot_manifest[filename.removesuffix(".png")] = str(path.relative_to(run_dir))
        plt.close(fig)

    manifest = {
        "packet_type": "correlator_effective_mass_diagnostic",
        "claim_boundary": config["claim_boundary"],
        "artifacts": {
            "config": "config.json",
            "observables": "observables.csv",
            "diagnostics": "diagnostics.json",
            "correlator": "correlator.csv",
            "effective_mass": "effective_mass.csv",
            "plots": plot_manifest,
        },
        "arrays": {
            "glueball_samples": "glueball_samples.npy",
        },
    }
    save_manifest_json(run_dir, manifest)
    print(f"Wrote correlator diagnostic run packet: {run_dir}")


if __name__ == "__main__":
    main()
