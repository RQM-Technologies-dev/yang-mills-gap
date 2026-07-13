import inspect

import numpy as np
import pytest

from yang_mills_gap.effective_mass import effective_mass, effective_mass_cosh
from yang_mills_gap.kgf_reference import (
    kgf_exponential_correlator,
    kgf_mass_recovery_diagnostics,
    kgf_periodic_correlator,
    kgf_spectral_correlator,
    sample_noisy_correlator_ensemble,
)
from yang_mills_gap.plateau import plateau_candidates


def test_infinite_time_exponential_recovers_inserted_log_mass() -> None:
    mass = 0.37
    corr = kgf_exponential_correlator(mass, np.arange(12))

    assert np.allclose(effective_mass(corr), mass)


def test_periodic_correlator_recovers_inserted_cosh_mass() -> None:
    mass = 0.43
    corr = kgf_periodic_correlator(mass, 16)
    estimated = effective_mass_cosh(corr)

    assert np.allclose(estimated[1:-1], mass)
    assert np.isnan(estimated[[0, -1]]).all()


def test_multistate_correlator_approaches_lowest_mass_at_late_times() -> None:
    corr = kgf_spectral_correlator([0.3, 1.1], [1.0, 3.0], 30, periodic=False)
    estimated = effective_mass(corr)

    assert estimated[0] > 0.6
    assert abs(estimated[20] - 0.3) < 1.0e-6


def test_larger_excited_state_amplitude_delays_apparent_plateau() -> None:
    low_contamination = effective_mass(
        kgf_spectral_correlator([0.3, 0.9], [1.0, 0.2], 24, periodic=False)
    )
    high_contamination = effective_mass(
        kgf_spectral_correlator([0.3, 0.9], [1.0, 5.0], 24, periodic=False)
    )
    tolerance = 0.01
    low_start = int(np.flatnonzero(np.abs(low_contamination - 0.3) < tolerance)[0])
    high_start = int(np.flatnonzero(np.abs(high_contamination - 0.3) < tolerance)[0])

    assert high_start > low_start


def test_synthetic_noise_has_uncertainty_and_can_destabilize_plateaus() -> None:
    corr = kgf_periodic_correlator(0.4, 14)
    ensemble = sample_noisy_correlator_ensemble(
        corr, n_samples=40, relative_noise=0.35, seed=20260712
    )
    masses = np.asarray([effective_mass_cosh(sample) for sample in ensemble])

    finite_column = masses[:, 4]
    assert np.std(finite_column[np.isfinite(finite_column)]) > 0.0
    noisy_mean_mass = effective_mass_cosh(np.mean(ensemble, axis=0))
    assert plateau_candidates(noisy_mean_mass, min_length=5, relative_tolerance=0.01) == []


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: kgf_exponential_correlator(0.0, [0, 1]), "strictly positive"),
        (lambda: kgf_exponential_correlator(0.2, [0, 1], amplitude=-1), "nonnegative"),
        (lambda: kgf_exponential_correlator(0.2, [[0, 1]]), "one-dimensional"),
        (lambda: kgf_periodic_correlator(0.2, 0), "positive"),
        (lambda: kgf_spectral_correlator([], [], 8), "at least one"),
        (lambda: kgf_spectral_correlator([0.2], [1.0, 2.0], 8), "matching lengths"),
        (lambda: kgf_spectral_correlator([-0.2], [1.0], 8), "strictly positive"),
        (lambda: kgf_spectral_correlator([0.2], [-1.0], 8), "nonnegative"),
        (
            lambda: sample_noisy_correlator_ensemble(
                [1.0, 0.5], n_samples=0, relative_noise=0.1, seed=1
            ),
            "positive",
        ),
        (
            lambda: sample_noisy_correlator_ensemble(
                [1.0, 0.5], n_samples=2, relative_noise=-0.1, seed=1
            ),
            "nonnegative",
        ),
    ],
)
def test_invalid_inputs_raise_useful_exceptions(call, message: str) -> None:
    with pytest.raises((TypeError, ValueError), match=message):
        call()


def test_diagnostics_reuse_estimators_and_report_recovery_errors() -> None:
    corr = kgf_periodic_correlator(0.5, 12)
    report = kgf_mass_recovery_diagnostics(corr, 0.5, plateau_min_length=3)

    assert np.allclose(report["effective_mass_cosh"][1:-1], 0.5)
    assert report["cosh_plateaus"]
    assert report["cosh_plateaus"][0]["absolute_recovery_error"] < 1.0e-12
    assert "not Yang--Mills mass-gap evidence" in report["claim_boundary"]


def test_module_docstring_states_calibration_claim_boundary() -> None:
    import yang_mills_gap.kgf_reference as module

    docstring = inspect.getdoc(module) or ""
    assert "calibration" in docstring
    assert "not evidence" in docstring
    assert "not alter the standard Wilson-action baseline" in docstring
