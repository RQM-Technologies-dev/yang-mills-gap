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
