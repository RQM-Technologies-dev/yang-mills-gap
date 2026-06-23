import numpy as np
import pytest

from yang_mills_gap.effective_mass import effective_mass, effective_mass_cosh


def test_effective_mass_cosh_recovers_constant_mass_for_cosh_correlator() -> None:
    mass = 0.4
    nt = 8
    times = np.arange(nt)
    corr = np.cosh(mass * (times - nt / 2))
    estimated = effective_mass_cosh(corr)
    assert np.allclose(estimated[1:-1], mass)
    assert np.isnan(estimated[0])
    assert np.isnan(estimated[-1])


def test_effective_mass_cosh_returns_nan_for_invalid_arguments() -> None:
    corr = np.array([1.0, 2.0, 1.0])
    estimated = effective_mass_cosh(corr)
    assert np.isnan(estimated[1])


def test_effective_mass_estimators_validate_input_rank() -> None:
    with pytest.raises(ValueError):
        effective_mass(np.ones((2, 2)))
    with pytest.raises(ValueError):
        effective_mass_cosh(np.ones((2, 2)))
