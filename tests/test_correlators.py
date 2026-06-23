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
