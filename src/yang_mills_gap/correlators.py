"""Temporal correlators for glueball-like observables."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def temporal_correlator(
    samples: ArrayLike,
    *,
    connected: bool = True,
) -> NDArray[np.float64]:
    """Compute ``C(dt) = <O(t) O(t+dt)>`` with periodic time averaging.

    Args:
        samples: one timeseries with shape ``(Nt,)`` or an ensemble with shape
            ``(n_samples, Nt)``.
        connected: subtract the ensemble mean before forming the correlator.
    """

    data = np.asarray(samples, dtype=float)
    if data.ndim == 1:
        data = data[np.newaxis, :]
    if data.ndim != 2:
        raise ValueError("samples must have shape (Nt,) or (n_samples, Nt)")

    centered = data - np.mean(data) if connected else data
    nt = centered.shape[1]
    corr = np.empty(nt, dtype=float)
    for dt in range(nt):
        corr[dt] = np.mean(centered * np.roll(centered, -dt, axis=1))
    return corr


def bootstrap_correlator(
    samples: ArrayLike,
    *,
    n_bootstrap: int = 500,
    connected: bool = True,
    seed: int | None = None,
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """Bootstrap temporal-correlator mean and standard error.

    Returns ``(mean, stderr, bootstrap_estimates)``. Resampling is performed
    over the ensemble/sample axis.
    """

    data = np.asarray(samples, dtype=float)
    if data.ndim == 1:
        data = data[np.newaxis, :]
    if data.ndim != 2:
        raise ValueError("samples must have shape (Nt,) or (n_samples, Nt)")
    if n_bootstrap <= 0:
        raise ValueError("n_bootstrap must be positive")

    rng = np.random.default_rng(seed)
    n_samples = data.shape[0]
    estimates = np.empty((n_bootstrap, data.shape[1]), dtype=float)
    for index in range(n_bootstrap):
        draw = rng.integers(0, n_samples, size=n_samples)
        estimates[index] = temporal_correlator(data[draw], connected=connected)
    return (
        np.mean(estimates, axis=0),
        np.std(estimates, axis=0, ddof=1) if n_bootstrap > 1 else np.zeros(data.shape[1]),
        estimates,
    )


def jackknife_correlator(
    samples: ArrayLike,
    *,
    connected: bool = True,
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """Jackknife temporal-correlator mean and standard error.

    Returns ``(mean, stderr, jackknife_estimates)``. At least two ensemble
    samples are required.
    """

    data = np.asarray(samples, dtype=float)
    if data.ndim != 2:
        raise ValueError("jackknife samples must have shape (n_samples, Nt)")
    n_samples = data.shape[0]
    if n_samples < 2:
        raise ValueError("jackknife requires at least two samples")

    estimates = np.empty((n_samples, data.shape[1]), dtype=float)
    for omitted in range(n_samples):
        estimates[omitted] = temporal_correlator(
            np.delete(data, omitted, axis=0),
            connected=connected,
        )

    mean = np.mean(estimates, axis=0)
    stderr = np.sqrt((n_samples - 1) * np.mean((estimates - mean) ** 2, axis=0))
    return mean, stderr, estimates
