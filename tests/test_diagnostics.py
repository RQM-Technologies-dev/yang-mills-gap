import numpy as np
import pytest

from yang_mills_gap.diagnostics import (
    autocorrelation,
    integrated_autocorrelation_time,
    running_mean,
    thermalization_window_summary,
)


def ar1_series(phi: float, n: int = 256) -> np.ndarray:
    values = np.empty(n, dtype=float)
    values[0] = 1.0
    for index in range(1, n):
        forcing = np.sin(0.37 * index)
        values[index] = phi * values[index - 1] + forcing
    return values


def test_running_mean_on_constant_series() -> None:
    values = np.full(5, 3.0)
    assert np.allclose(running_mean(values), 3.0)


def test_autocorrelation_constant_series_is_defined_at_zero_lag() -> None:
    rho = autocorrelation(np.full(6, 2.0), max_lag=4)
    assert np.allclose(rho, np.array([1.0, 0.0, 0.0, 0.0, 0.0]))
    assert integrated_autocorrelation_time(np.full(6, 2.0)) == 0.5


def test_autocorrelation_white_noise_has_small_lag_average() -> None:
    rng = np.random.default_rng(1234)
    values = rng.normal(size=512)
    rho = autocorrelation(values, max_lag=20)
    assert rho.shape == (21,)
    assert np.isclose(rho[0], 1.0)
    assert abs(float(np.mean(rho[1:]))) < 0.15


def test_integrated_autocorrelation_time_is_larger_for_correlated_series() -> None:
    rng = np.random.default_rng(5678)
    white_noise = rng.normal(size=256)
    correlated = ar1_series(phi=0.85, n=256)

    assert integrated_autocorrelation_time(correlated) > integrated_autocorrelation_time(white_noise)


def test_thermalization_window_summary_tracks_post_cut_means() -> None:
    values = np.concatenate([np.full(10, 5.0), np.full(30, 2.0)])
    summary = thermalization_window_summary(values, cut_fractions=(0.0, 0.25, 0.5))

    assert [row["cut_fraction"] for row in summary] == [0.0, 0.25, 0.5]
    assert summary[0]["n_samples"] == 40.0
    assert summary[1]["mean"] < summary[0]["mean"]
    assert np.isclose(summary[2]["mean"], 2.0)


def test_diagnostics_validate_inputs() -> None:
    with pytest.raises(ValueError):
        running_mean(np.ones((2, 2)))
    with pytest.raises(ValueError):
        autocorrelation(np.ones(4), max_lag=-1)
    with pytest.raises(ValueError):
        integrated_autocorrelation_time(np.ones(4), c=0)
    with pytest.raises(ValueError):
        thermalization_window_summary(np.ones(3), cut_fractions=(1.0,))
