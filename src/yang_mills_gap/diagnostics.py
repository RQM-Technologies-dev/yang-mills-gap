"""Basic Markov-chain diagnostics for tiny exploratory runs."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from numpy.typing import ArrayLike, NDArray


def running_mean(series: ArrayLike) -> NDArray[np.float64]:
    """Return the cumulative running mean of a one-dimensional series."""

    values = np.asarray(series, dtype=float)
    if values.ndim != 1:
        raise ValueError("series must be one-dimensional")
    if values.size == 0:
        raise ValueError("series must not be empty")
    return np.cumsum(values) / np.arange(1, values.size + 1)


def integrated_autocorrelation_time(series: ArrayLike, *, max_lag: int | None = None) -> float:
    """Estimate integrated autocorrelation time with a positive-sequence cutoff."""

    values = np.asarray(series, dtype=float)
    if values.ndim != 1:
        raise ValueError("series must be one-dimensional")
    if values.size < 2:
        raise ValueError("series must contain at least two values")
    if max_lag is not None and max_lag < 0:
        raise ValueError("max_lag must be nonnegative")

    centered = values - np.mean(values)
    variance = float(np.dot(centered, centered) / values.size)
    if variance == 0.0:
        return 0.5

    max_available_lag = values.size - 1
    lag_limit = max_available_lag if max_lag is None else min(max_lag, max_available_lag)
    tau = 0.5
    for lag in range(1, lag_limit + 1):
        autocov = float(np.dot(centered[:-lag], centered[lag:]) / (values.size - lag))
        rho = autocov / variance
        if rho <= 0.0:
            break
        tau += rho
    return float(tau)


def plot_thermalization(
    series: ArrayLike,
    *,
    output_path: str | Path | None = None,
    discard: int = 0,
    ylabel: str = "observable",
    title: str = "Thermalization diagnostic",
):
    """Create a simple time-series plus running-mean thermalization plot."""

    import matplotlib.pyplot as plt

    values = np.asarray(series, dtype=float)
    if values.ndim != 1:
        raise ValueError("series must be one-dimensional")
    if discard < 0:
        raise ValueError("discard must be nonnegative")
    if discard >= values.size:
        raise ValueError("discard must be smaller than the series length")

    means = running_mean(values)
    x = np.arange(values.size)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(x, values, marker="o", linewidth=1.0, label=ylabel)
    ax.plot(x, means, linewidth=1.8, label="running mean")
    if discard:
        ax.axvline(discard, color="black", linestyle="--", linewidth=1.0, label="discard")
    ax.set_xlabel("sample")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()

    if output_path is not None:
        fig.savefig(output_path, dpi=160)
    return fig, ax
