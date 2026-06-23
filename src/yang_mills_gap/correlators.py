"""Temporal correlators for glueball-like observables."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def temporal_correlator(
    samples: ArrayLike,
    *,
    connected: bool = True,
    mean_mode: str = "global",
) -> NDArray[np.float64]:
    """Compute ``C(dt) = <O(t) O(t+dt)>`` with periodic time averaging.

    Args:
        samples: one timeseries with shape ``(Nt,)`` or an ensemble with shape
            ``(n_samples, Nt)``.
        connected: subtract the ensemble mean before forming the correlator.
        mean_mode: ``"global"`` subtracts one mean over all samples and times.
            ``"per_time"`` and ``"ensemble"`` subtract the ensemble mean for
            each time slice. For a single timeseries, these per-time modes
            produce a zero connected correlator because each time point is its
            own one-sample ensemble mean.
    """

    data = np.asarray(samples, dtype=float)
    if data.ndim == 1:
        data = data[np.newaxis, :]
    if data.ndim != 2:
        raise ValueError("samples must have shape (Nt,) or (n_samples, Nt)")

    if mean_mode not in {"global", "per_time", "ensemble"}:
        raise ValueError("mean_mode must be 'global', 'per_time', or 'ensemble'")

    if not connected:
        centered = data
    elif mean_mode == "global":
        centered = data - np.mean(data)
    else:
        centered = data - np.mean(data, axis=0, keepdims=True)
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
    mean_mode: str = "global",
    seed: int | None = None,
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """Bootstrap temporal-correlator mean and standard error.

    Returns ``(mean, stderr, bootstrap_estimates)``. Resampling is performed
    over the ensemble/sample axis. If only one ensemble sample is available, or
    if ``n_bootstrap == 1``, the returned standard error is exactly zero.
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
        estimates[index] = temporal_correlator(data[draw], connected=connected, mean_mode=mean_mode)
    if n_bootstrap == 1 or n_samples == 1:
        stderr = np.zeros(data.shape[1], dtype=float)
    else:
        stderr = np.std(estimates, axis=0, ddof=1)
    return (
        np.mean(estimates, axis=0),
        stderr,
        estimates,
    )


def jackknife_correlator(
    samples: ArrayLike,
    *,
    connected: bool = True,
    mean_mode: str = "global",
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
            mean_mode=mean_mode,
        )

    mean = np.mean(estimates, axis=0)
    stderr = np.sqrt((n_samples - 1) * np.mean((estimates - mean) ** 2, axis=0))
    return mean, stderr, estimates
