"""Effective-mass estimators from temporal correlators."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def effective_mass(correlator: ArrayLike) -> NDArray[np.float64]:
    """Return ``m_eff(t) = log(C(t) / C(t+1))`` where the ratio is positive."""

    corr = np.asarray(correlator, dtype=float)
    if corr.ndim != 1:
        raise ValueError("correlator must be one-dimensional")
    if corr.size < 2:
        raise ValueError("correlator must contain at least two time separations")
    numer = corr[:-1]
    denom = corr[1:]
    result = np.full(corr.size - 1, np.nan, dtype=float)
    valid = (numer > 0.0) & (denom > 0.0)
    result[valid] = np.log(numer[valid] / denom[valid])
    return result
