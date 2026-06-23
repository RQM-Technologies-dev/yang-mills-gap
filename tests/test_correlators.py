import numpy as np
import pytest

from yang_mills_gap.correlators import bootstrap_correlator, jackknife_correlator, temporal_correlator


def test_bootstrap_correlator_shapes() -> None:
    rng = np.random.default_rng(111)
    samples = rng.normal(size=(6, 4))
    mean, stderr, estimates = bootstrap_correlator(samples, n_bootstrap=10, seed=222)

    assert mean.shape == (4,)
    assert stderr.shape == (4,)
    assert estimates.shape == (10, 4)
    assert np.all(np.isfinite(mean))
    assert np.all(stderr >= 0.0)


def test_bootstrap_single_draw_returns_zero_stderr() -> None:
    rng = np.random.default_rng(112)
    samples = rng.normal(size=(5, 4))
    mean, stderr, estimates = bootstrap_correlator(samples, n_bootstrap=1, seed=223)

    assert mean.shape == (4,)
    assert estimates.shape == (1, 4)
    assert np.allclose(stderr, 0.0)


def test_bootstrap_single_sample_returns_zero_stderr() -> None:
    samples = np.array([[1.0, 2.0, 4.0, 8.0]])
    _, stderr, estimates = bootstrap_correlator(samples, n_bootstrap=8, connected=False, seed=224)

    assert estimates.shape == (8, 4)
    assert np.allclose(stderr, 0.0)


def test_jackknife_correlator_shapes() -> None:
    rng = np.random.default_rng(333)
    samples = rng.normal(size=(5, 4))
    mean, stderr, estimates = jackknife_correlator(samples)

    assert mean.shape == (4,)
    assert stderr.shape == (4,)
    assert estimates.shape == (5, 4)
    assert np.all(np.isfinite(mean))
    assert np.all(stderr >= 0.0)


def test_jackknife_requires_an_ensemble() -> None:
    with pytest.raises(ValueError):
        jackknife_correlator(np.ones(4))
    with pytest.raises(ValueError):
        jackknife_correlator(np.ones((1, 4)))


def test_temporal_correlator_still_accepts_single_timeseries() -> None:
    corr = temporal_correlator(np.array([1.0, 2.0, 3.0]), connected=False)
    assert corr.shape == (3,)


def test_temporal_correlator_mean_modes() -> None:
    samples = np.array([[1.0, 2.0, 3.0], [3.0, 4.0, 5.0]])
    global_corr = temporal_correlator(samples, connected=True, mean_mode="global")
    per_time_corr = temporal_correlator(samples, connected=True, mean_mode="per_time")
    ensemble_corr = temporal_correlator(samples, connected=True, mean_mode="ensemble")

    assert global_corr.shape == (3,)
    assert per_time_corr.shape == (3,)
    assert np.allclose(per_time_corr, ensemble_corr)


def test_temporal_correlator_rejects_unknown_mean_mode() -> None:
    with pytest.raises(ValueError):
        temporal_correlator(np.ones((2, 3)), mean_mode="unknown")
