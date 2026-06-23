"""Basic finite-chain diagnostics for exploratory lattice runs."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def _as_1d_series(series: ArrayLike) -> NDArray[np.float64]:
    values = np.asarray(series, dtype=float)
    if values.ndim != 1:
        raise ValueError("series must be one-dimensional")
    if values.size == 0:
        raise ValueError("series must not be empty")
    return values


def running_mean(series: ArrayLike) -> NDArray[np.float64]:
    """Return the cumulative running mean of a one-dimensional series."""

    values = _as_1d_series(series)
    return np.cumsum(values) / np.arange(1, values.size + 1)


def autocorrelation(series: ArrayLike, max_lag: int | None = None) -> NDArray[np.float64]:
    """Return normalized autocorrelation values from lag 0 through ``max_lag``."""

    values = _as_1d_series(series)
    if max_lag is not None and max_lag < 0:
        raise ValueError("max_lag must be nonnegative")

    lag_limit = values.size - 1 if max_lag is None else min(max_lag, values.size - 1)
    centered = values - np.mean(values)
    norm = float(np.dot(centered, centered))
    result = np.zeros(lag_limit + 1, dtype=float)
    result[0] = 1.0
    if norm == 0.0:
        return result

    for lag in range(1, lag_limit + 1):
        result[lag] = float(np.dot(centered[:-lag], centered[lag:]) / norm)
    return result


def integrated_autocorrelation_time(series: ArrayLike, c: float = 5.0) -> float:
    """Estimate integrated autocorrelation time using a self-consistent window."""

    if c <= 0:
        raise ValueError("c must be positive")

    rho = autocorrelation(series)
    tau = 0.5
    for lag in range(1, rho.size):
        if rho[lag] <= 0.0:
            break
        tau += float(rho[lag])
        if lag >= c * tau:
            break
    return float(tau)


def thermalization_window_summary(
    series: ArrayLike,
    cut_fractions: tuple[float, ...] = (0.0, 0.1, 0.2, 0.3),
) -> list[dict[str, float]]:
    """Summarize post-cut means and standard errors for simple burn-in checks."""

    values = _as_1d_series(series)
    summaries: list[dict[str, float]] = []
    for fraction in cut_fractions:
        if not 0.0 <= fraction < 1.0:
            raise ValueError("cut fractions must be in [0, 1)")
        start = int(np.floor(fraction * values.size))
        window = values[start:]
        stderr = 0.0 if window.size < 2 else float(np.std(window, ddof=1) / np.sqrt(window.size))
        summaries.append(
            {
                "cut_fraction": float(fraction),
                "start_index": float(start),
                "n_samples": float(window.size),
                "mean": float(np.mean(window)),
                "stderr": stderr,
            }
        )
    return summaries
