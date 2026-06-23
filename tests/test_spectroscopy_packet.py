import csv

import numpy as np

from yang_mills_gap.spectroscopy_packet import (
    compute_correlator_artifacts,
    make_correlator_records,
    make_effective_mass_records,
    write_correlator_packet,
)


def synthetic_samples() -> np.ndarray:
    base = np.array([1.0, 0.8, 0.6, 0.8])
    return np.vstack([base + 0.02 * index for index in range(6)])


def test_compute_correlator_artifacts_returns_expected_shapes() -> None:
    artifacts = compute_correlator_artifacts(synthetic_samples(), n_bootstrap=5, seed=123)

    assert set(artifacts) == {"correlator", "correlator_stderr", "effective_mass_log", "effective_mass_cosh"}
    assert artifacts["correlator"].shape == (4,)
    assert artifacts["correlator_stderr"].shape == (4,)
    assert artifacts["effective_mass_log"].shape == (3,)
    assert artifacts["effective_mass_cosh"].shape == (4,)
    assert np.all(np.isfinite(artifacts["correlator"]))


def test_make_correlator_records_are_csv_safe() -> None:
    records = make_correlator_records(np.array([1.0, np.nan]), np.array([0.1, np.inf]))

    assert records == [
        {"t": 0.0, "connected_correlator": 1.0, "bootstrap_stderr": 0.1},
        {"t": 1.0, "connected_correlator": "", "bootstrap_stderr": ""},
    ]


def test_make_effective_mass_records_handles_different_lengths() -> None:
    records = make_effective_mass_records(np.array([0.5, np.nan]), np.array([np.nan, 0.4, 0.3]))

    assert records[0] == {"t": 0.0, "m_eff_log": 0.5, "m_eff_cosh": ""}
    assert records[1] == {"t": 1.0, "m_eff_log": "", "m_eff_cosh": 0.4}
    assert records[2] == {"t": 2.0, "m_eff_log": "", "m_eff_cosh": 0.3}


def test_write_correlator_packet_creates_required_files(tmp_path) -> None:
    records = [
        {"sweep": 1.0, "action": 2.0, "average_plaquette": 0.1, "average_closure_defect": 0.9, "acceptance_rate": 0.8},
        {"sweep": 2.0, "action": 1.8, "average_plaquette": 0.2, "average_closure_defect": 0.8, "acceptance_rate": 0.9},
    ]
    config = {
        "label": "synthetic spectroscopy packet",
        "research_objective": "test packet writer",
        "claim_boundary": "diagnostic only",
    }
    run_dir = write_correlator_packet(tmp_path / "packet", config, records, synthetic_samples(), n_bootstrap=3, seed=456)

    expected = [
        "config.json",
        "manifest.json",
        "observables.csv",
        "diagnostics.json",
        "glueball_samples.npy",
        "correlator.csv",
        "effective_mass.csv",
        "plots/action_running_mean.png",
        "plots/closure_running_mean.png",
        "plots/action_autocorrelation.png",
        "plots/closure_autocorrelation.png",
        "plots/action_thermalization_windows.png",
        "plots/closure_thermalization_windows.png",
        "plots/correlator.png",
        "plots/effective_mass.png",
    ]
    for relative_path in expected:
        assert (run_dir / relative_path).exists()

    with (run_dir / "effective_mass.csv").open(newline="", encoding="utf-8") as handle:
        assert list(csv.DictReader(handle))
