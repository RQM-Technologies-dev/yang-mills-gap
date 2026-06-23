"""Correlator and effective-mass diagnostic packet helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from .correlators import bootstrap_correlator, temporal_correlator
from .diagnostics import autocorrelation, integrated_autocorrelation_time, running_mean, thermalization_window_summary
from .effective_mass import effective_mass, effective_mass_cosh
from .packet_plots import (
    plot_autocorrelation,
    plot_correlator,
    plot_effective_mass,
    plot_running_mean,
    plot_thermalization,
)
from .run_packet import save_array, save_config_json, save_diagnostics_json, save_figure, save_manifest_json, save_records_csv


def compute_correlator_artifacts(
    samples: np.ndarray,
    n_bootstrap: int = 100,
    seed: int | None = None,
    mean_mode: str = "global",
) -> dict[str, np.ndarray]:
    """Compute connected correlator, bootstrap stderr, and effective masses."""

    sample_array = np.asarray(samples, dtype=float)
    correlator = temporal_correlator(sample_array, connected=True, mean_mode=mean_mode)
    _, correlator_stderr, _ = bootstrap_correlator(
        sample_array,
        n_bootstrap=n_bootstrap,
        connected=True,
        mean_mode=mean_mode,
        seed=seed,
    )
    return {
        "correlator": correlator,
        "correlator_stderr": correlator_stderr,
        "effective_mass_log": effective_mass(correlator),
        "effective_mass_cosh": effective_mass_cosh(correlator),
    }


def _csv_number(value: float) -> float | str:
    return "" if not np.isfinite(value) else float(value)


def make_correlator_records(correlator: np.ndarray, stderr: np.ndarray) -> list[dict[str, float | str]]:
    """Return CSV-safe correlator records."""

    if correlator.shape != stderr.shape:
        raise ValueError("correlator and stderr must have matching shapes")
    return [
        {
            "t": float(index),
            "connected_correlator": _csv_number(float(correlator[index])),
            "bootstrap_stderr": _csv_number(float(stderr[index])),
        }
        for index in range(correlator.size)
    ]


def make_effective_mass_records(mass_log: np.ndarray, mass_cosh: np.ndarray) -> list[dict[str, float | str]]:
    """Return CSV-safe effective-mass records."""

    n_rows = max(mass_log.size, mass_cosh.size)
    records: list[dict[str, float | str]] = []
    for index in range(n_rows):
        log_value = _csv_number(float(mass_log[index])) if index < mass_log.size else ""
        cosh_value = _csv_number(float(mass_cosh[index])) if index < mass_cosh.size else ""
        records.append(
            {
                "t": float(index),
                "m_eff_log": log_value,
                "m_eff_cosh": cosh_value,
            }
        )
    return records


def series_diagnostics(values: np.ndarray) -> dict[str, Any]:
    """Return running, autocorrelation, IAT, and thermalization diagnostics."""

    max_lag = min(10, values.size - 1)
    return {
        "running_mean": running_mean(values).tolist(),
        "autocorrelation": autocorrelation(values, max_lag=max_lag).tolist(),
        "integrated_autocorrelation_time": integrated_autocorrelation_time(values),
        "thermalization_windows": thermalization_window_summary(values),
    }


def diagnostics_from_records(records: list[dict[str, float]], artifacts: dict[str, np.ndarray], config: dict[str, Any]) -> dict[str, Any]:
    """Build packet diagnostics from observable records and correlator artifacts."""

    action = np.array([record["action"] for record in records], dtype=float)
    closure = np.array([record["average_closure_defect"] for record in records], dtype=float)
    acceptance = np.array([record["acceptance_rate"] for record in records], dtype=float)
    return {
        "action": series_diagnostics(action),
        "average_closure_defect": series_diagnostics(closure),
        "correlator": {
            "n_samples": float(config.get("n_samples", len(records))),
            "nt": float(artifacts["correlator"].size),
            "bootstrap_stderr_mean": float(np.mean(artifacts["correlator_stderr"])),
            "mean_mode": str(config.get("mean_mode", "global")),
        },
        "summary": {
            "n_measurements": float(len(records)),
            "mean_acceptance_rate": float(np.mean(acceptance)),
            "research_objective": config.get("research_objective", ""),
            "claim_boundary": config.get("claim_boundary", "diagnostic only; not a mass-gap estimate"),
        },
    }


def write_correlator_packet(
    run_dir: str | Path,
    config: dict[str, Any],
    records: list[dict[str, float]],
    glueball_samples: np.ndarray,
    *,
    n_bootstrap: int = 100,
    seed: int | None = None,
    mean_mode: str = "global",
) -> Path:
    """Write a complete correlator/effective-mass diagnostic packet."""

    root = Path(run_dir)
    root.mkdir(parents=True, exist_ok=True)
    (root / "plots").mkdir(parents=True, exist_ok=True)
    sample_array = np.asarray(glueball_samples, dtype=float)
    artifacts = compute_correlator_artifacts(sample_array, n_bootstrap=n_bootstrap, seed=seed, mean_mode=mean_mode)
    enriched_config = dict(config)
    enriched_config["n_samples"] = int(sample_array.shape[0])
    enriched_config["mean_mode"] = mean_mode
    diagnostics = diagnostics_from_records(records, artifacts, enriched_config)

    save_config_json(root / "config.json", enriched_config)
    save_records_csv(root / "observables.csv", records)
    save_diagnostics_json(root / "diagnostics.json", diagnostics)
    save_array(root / "glueball_samples.npy", sample_array)
    save_records_csv(root / "correlator.csv", make_correlator_records(artifacts["correlator"], artifacts["correlator_stderr"]))
    save_records_csv(
        root / "effective_mass.csv",
        make_effective_mass_records(artifacts["effective_mass_log"], artifacts["effective_mass_cosh"]),
    )

    action = np.array([record["action"] for record in records], dtype=float)
    closure = np.array([record["average_closure_defect"] for record in records], dtype=float)
    plot_specs = [
        (plot_running_mean(action, diagnostics["action"]["running_mean"], "action", "Action running mean"), "action_running_mean.png"),
        (
            plot_running_mean(
                closure,
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
        (plot_effective_mass(artifacts["effective_mass_log"], artifacts["effective_mass_cosh"]), "effective_mass.png"),
    ]

    plot_manifest: dict[str, str] = {}
    for fig, filename in plot_specs:
        path = save_figure(root, fig, filename)
        plot_manifest[filename.removesuffix(".png")] = str(path.relative_to(root))
        try:
            import matplotlib.pyplot as plt

            plt.close(fig)
        except Exception:
            pass

    manifest = {
        "packet_type": "correlator_effective_mass_diagnostic",
        "research_objective": enriched_config.get("research_objective", ""),
        "claim_boundary": enriched_config.get("claim_boundary", "diagnostic only; not a mass-gap estimate"),
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
    save_manifest_json(root, manifest)
    return root
