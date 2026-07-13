"""Klein--Gordon--Fock correlators for diagnostic calibration only.

This module provides a massive scalar reference model for checking correlator,
effective-mass, and plateau machinery. Synthetic KGF output is not Yang--Mills
data, does not alter the standard Wilson-action baseline, and is not evidence
for or proof of the Yang--Mills mass gap. The positive masses used here are
inputs; their dynamical origin is not derived by these utilities.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .effective_mass import effective_mass, effective_mass_cosh
from .plateau import summarize_plateau_candidates


def _positive_mass(value: float, *, name: str = "mass") -> float:
    mass = float(value)
    if not np.isfinite(mass) or mass <= 0.0:
        raise ValueError(f"{name} must be finite and strictly positive")
    return mass


def _nonnegative_amplitude(value: float, *, name: str = "amplitude") -> float:
    amplitude = float(value)
    if not np.isfinite(amplitude) or amplitude < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return amplitude


def _temporal_extent(value: int) -> int:
    if isinstance(value, (bool, np.bool_)) or not isinstance(
        value, (int, np.integer)
    ):
        raise TypeError("temporal_extent must be an integer")
    extent = int(value)
    if extent <= 0:
        raise ValueError("temporal_extent must be positive")
    return extent


def kgf_exponential_correlator(
    mass: float,
    times: ArrayLike,
    *,
    amplitude: float = 1.0,
) -> NDArray[np.float64]:
    """Return ``C(t) = amplitude * exp(-mass * t)`` with shape ``(n_times,)``.

    Times must be a nonempty one-dimensional array of finite, nonnegative
    Euclidean separations. With the default amplitude, ``C(0)`` is normalized
    to one whenever zero is included.
    """

    checked_mass = _positive_mass(mass)
    checked_amplitude = _nonnegative_amplitude(amplitude)
    time_array = np.asarray(times, dtype=float)
    if time_array.ndim != 1 or time_array.size == 0:
        raise ValueError("times must be a nonempty one-dimensional array")
    if not np.all(np.isfinite(time_array)) or np.any(time_array < 0.0):
        raise ValueError("times must contain finite, nonnegative separations")
    return np.asarray(
        checked_amplitude * np.exp(-checked_mass * time_array), dtype=float
    )


def kgf_periodic_correlator(
    mass: float,
    temporal_extent: int,
    *,
    amplitude: float = 1.0,
) -> NDArray[np.float64]:
    """Return a forward-plus-backward periodic correlator with shape ``(T,)``.

    The discrete convention is
    ``C(t) = A [exp(-m t) + exp(-m (T - t))]`` for ``t = 0, ..., T - 1``.
    It is the periodic cosh convention consumed by :func:`effective_mass_cosh`.
    """

    checked_mass = _positive_mass(mass)
    extent = _temporal_extent(temporal_extent)
    checked_amplitude = _nonnegative_amplitude(amplitude)
    times = np.arange(extent, dtype=float)
    return np.asarray(
        checked_amplitude
        * (np.exp(-checked_mass * times) + np.exp(-checked_mass * (extent - times))),
        dtype=float,
    )


def kgf_spectral_correlator(
    masses: ArrayLike,
    amplitudes: ArrayLike,
    temporal_extent: int,
    *,
    periodic: bool = True,
) -> NDArray[np.float64]:
    """Return a deterministic multi-state spectral correlator with shape ``(T,)``.

    ``masses`` and ``amplitudes`` must be matching nonempty one-dimensional
    arrays. Every mass is strictly positive and every spectral amplitude is
    nonnegative. Each state contributes a periodic cosh correlator when
    ``periodic`` is true and a forward exponential otherwise.
    """

    extent = _temporal_extent(temporal_extent)
    mass_array = np.asarray(masses, dtype=float)
    amplitude_array = np.asarray(amplitudes, dtype=float)
    if mass_array.ndim != 1 or amplitude_array.ndim != 1:
        raise ValueError("masses and amplitudes must be one-dimensional")
    if mass_array.size == 0:
        raise ValueError("at least one spectral state is required")
    if mass_array.shape != amplitude_array.shape:
        raise ValueError("masses and amplitudes must have matching lengths")
    if not np.all(np.isfinite(mass_array)) or np.any(mass_array <= 0.0):
        raise ValueError("all masses must be finite and strictly positive")
    if not np.all(np.isfinite(amplitude_array)) or np.any(amplitude_array < 0.0):
        raise ValueError("all amplitudes must be finite and nonnegative")
    if not isinstance(periodic, (bool, np.bool_)):
        raise TypeError("periodic must be a boolean")

    times = np.arange(extent, dtype=float)
    forward = np.exp(-mass_array[:, np.newaxis] * times[np.newaxis, :])
    contributions = amplitude_array[:, np.newaxis] * forward
    if periodic:
        contributions += amplitude_array[:, np.newaxis] * np.exp(
            -mass_array[:, np.newaxis] * (extent - times)[np.newaxis, :]
        )
    return np.asarray(np.sum(contributions, axis=0), dtype=float)


def sample_noisy_correlator_ensemble(
    correlator: ArrayLike,
    *,
    n_samples: int,
    relative_noise: float,
    seed: int,
) -> NDArray[np.float64]:
    """Return synthetic independent noisy copies with shape ``(n_samples, T)``.

    Gaussian noise at each time has standard deviation
    ``relative_noise * abs(C(t))``. The result is calibration data, not a model
    of Yang--Mills Monte Carlo correlations.
    """

    corr = np.asarray(correlator, dtype=float)
    if corr.ndim != 1 or corr.size == 0:
        raise ValueError("correlator must be a nonempty one-dimensional array")
    if not np.all(np.isfinite(corr)):
        raise ValueError("correlator must contain only finite values")
    if isinstance(n_samples, (bool, np.bool_)) or not isinstance(
        n_samples, (int, np.integer)
    ):
        raise TypeError("n_samples must be an integer")
    if int(n_samples) <= 0:
        raise ValueError("n_samples must be positive")
    noise = float(relative_noise)
    if not np.isfinite(noise) or noise < 0.0:
        raise ValueError("relative_noise must be finite and nonnegative")
    if isinstance(seed, (bool, np.bool_)) or not isinstance(seed, (int, np.integer)):
        raise TypeError("seed must be an integer")

    rng = np.random.default_rng(int(seed))
    perturbations = rng.normal(
        scale=noise * np.abs(corr), size=(int(n_samples), corr.size)
    )
    return np.asarray(corr[np.newaxis, :] + perturbations, dtype=float)


def kgf_mass_recovery_diagnostics(
    correlator: ArrayLike,
    inserted_mass: float,
    *,
    plateau_min_length: int = 2,
    plateau_relative_tolerance: float = 0.05,
) -> dict[str, Any]:
    """Compare existing mass estimators with a known synthetic KGF mass.

    The returned dictionary contains the log and cosh effective-mass arrays,
    their plateau summaries, and absolute/relative errors for every plateau.
    This helper delegates estimator and plateau behavior to the repository's
    existing implementations.
    """

    mass = _positive_mass(inserted_mass, name="inserted_mass")
    corr = np.asarray(correlator, dtype=float)
    if corr.ndim != 1 or corr.size < 3:
        raise ValueError("correlator must be one-dimensional with at least three values")

    log_values = effective_mass(corr)
    cosh_values = effective_mass_cosh(corr)

    def summaries(values: NDArray[np.float64]) -> list[dict[str, Any]]:
        result = summarize_plateau_candidates(
            values,
            min_length=plateau_min_length,
            relative_tolerance=plateau_relative_tolerance,
        )
        for item in result:
            item["absolute_recovery_error"] = abs(float(item["mean"]) - mass)
            item["relative_recovery_error"] = item["absolute_recovery_error"] / mass
        return result

    return {
        "claim_boundary": (
            "Synthetic KGF calibration only; not Yang--Mills mass-gap evidence."
        ),
        "inserted_mass": mass,
        "effective_mass_log": log_values,
        "effective_mass_cosh": cosh_values,
        "log_plateaus": summaries(log_values),
        "cosh_plateaus": summaries(cosh_values),
    }
