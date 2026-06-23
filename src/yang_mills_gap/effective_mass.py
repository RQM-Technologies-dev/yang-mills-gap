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


def effective_mass_cosh(correlator: ArrayLike) -> NDArray[np.float64]:
    """Return the symmetric cosh effective-mass estimator.

    ``m_eff(t) = arccosh((C(t-1) + C(t+1)) / (2 C(t)))`` is evaluated for
    interior time slices. Endpoints and invalid arccosh arguments return NaN.
    """

    corr = np.asarray(correlator, dtype=float)
    if corr.ndim != 1:
        raise ValueError("correlator must be one-dimensional")
    if corr.size < 3:
        raise ValueError("correlator must contain at least three time separations")

    result = np.full(corr.size, np.nan, dtype=float)
    denom = 2.0 * corr[1:-1]
    with np.errstate(divide="ignore", invalid="ignore"):
        argument = (corr[:-2] + corr[2:]) / denom
    valid = np.isfinite(argument) & (argument >= 1.0)
    interior = result[1:-1]
    interior[valid] = np.arccosh(argument[valid])
    return result
