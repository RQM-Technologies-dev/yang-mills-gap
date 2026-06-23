import numpy as np
import pytest

from yang_mills_gap.diagnostics import integrated_autocorrelation_time, plot_thermalization, running_mean


def test_running_mean_on_synthetic_series() -> None:
    values = np.array([1.0, 3.0, 5.0, 7.0])
    assert np.allclose(running_mean(values), np.array([1.0, 2.0, 3.0, 4.0]))


def test_integrated_autocorrelation_time_for_alternating_series_uses_positive_cutoff() -> None:
    values = np.array([1.0, -1.0] * 8)
    assert np.isclose(integrated_autocorrelation_time(values), 0.5)


def test_integrated_autocorrelation_time_detects_positive_correlation() -> None:
    values = np.linspace(0.0, 1.0, 16)
    assert integrated_autocorrelation_time(values, max_lag=3) > 0.5


def test_thermalization_plot_helper_writes_file(tmp_path) -> None:
    path = tmp_path / "thermalization.png"
    fig, _ = plot_thermalization(np.array([3.0, 2.0, 1.5, 1.25]), output_path=path, discard=1)
    assert path.exists()
    fig.clf()


def test_diagnostics_validate_inputs() -> None:
    with pytest.raises(ValueError):
        running_mean(np.ones((2, 2)))
    with pytest.raises(ValueError):
        integrated_autocorrelation_time(np.ones(1))
    with pytest.raises(ValueError):
        integrated_autocorrelation_time(np.ones(4), max_lag=-1)
    with pytest.raises(ValueError):
        plot_thermalization(np.ones(3), discard=3)
