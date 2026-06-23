"""Shared finite-lattice diagnostic-chain driver."""

from __future__ import annotations

from typing import Any

import numpy as np

from .diagnostics import autocorrelation, integrated_autocorrelation_time, running_mean, thermalization_window_summary
from .lattice import Lattice4D
from .monte_carlo import run_metropolis


def _series_diagnostics(values: np.ndarray) -> dict[str, Any]:
    max_lag = min(10, values.size - 1)
    return {
        "running_mean": running_mean(values).tolist(),
        "autocorrelation": autocorrelation(values, max_lag=max_lag).tolist(),
        "integrated_autocorrelation_time": integrated_autocorrelation_time(values),
        "thermalization_windows": thermalization_window_summary(values),
    }


def run_chain(
    lattice_shape: tuple[int, int, int, int],
    beta: float,
    n_sweeps: int,
    step_size: float,
    thermalization: int,
    measure_every: int,
    hot_start: bool,
    use_local_action: bool,
    seed: int | None,
) -> dict[str, Any]:
    """Run a tiny baseline chain and return records plus diagnostic summaries."""

    lattice = Lattice4D(lattice_shape)
    field, records = run_metropolis(
        lattice,
        beta,
        n_sweeps=n_sweeps,
        step_size=step_size,
        thermalization=thermalization,
        measure_every=measure_every,
        hot_start=hot_start,
        use_local_action=use_local_action,
        seed=seed,
    )
    if not records:
        raise ValueError("chain produced no measurements; lower thermalization or measure_every")

    action = np.array([record["action"] for record in records], dtype=float)
    closure = np.array([record["average_closure_defect"] for record in records], dtype=float)
    plaquette = np.array([record["average_plaquette"] for record in records], dtype=float)
    acceptance = np.array([record["acceptance_rate"] for record in records], dtype=float)
    diagnostics = {
        "action": _series_diagnostics(action),
        "average_closure_defect": _series_diagnostics(closure),
        "summary": {
            "n_measurements": float(len(records)),
            "final_action": float(action[-1]),
            "final_average_plaquette": float(plaquette[-1]),
            "final_average_closure_defect": float(closure[-1]),
            "mean_acceptance_rate": float(np.mean(acceptance)),
            "use_local_action": bool(use_local_action),
        },
    }
    return {
        "field": field,
        "records": records,
        "diagnostics": diagnostics,
    }
