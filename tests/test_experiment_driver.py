import numpy as np

from yang_mills_gap.experiment_driver import run_chain


def test_experiment_driver_returns_expected_keys() -> None:
    result = run_chain(
        lattice_shape=(1, 1, 1, 2),
        beta=2.0,
        n_sweeps=4,
        step_size=0.2,
        thermalization=1,
        measure_every=1,
        hot_start=False,
        use_local_action=True,
        seed=123,
    )

    assert {"field", "records", "diagnostics"} <= result.keys()
    assert len(result["records"]) == 3
    first_record = result["records"][0]
    assert {"action", "average_plaquette", "average_closure_defect", "acceptance_rate"} <= first_record.keys()

    diagnostics = result["diagnostics"]
    assert {"action", "average_closure_defect", "summary"} <= diagnostics.keys()
    for key in ["action", "average_closure_defect"]:
        assert {"running_mean", "autocorrelation", "integrated_autocorrelation_time", "thermalization_windows"} <= diagnostics[key].keys()
        assert np.all(np.isfinite(diagnostics[key]["running_mean"]))
        assert np.all(np.isfinite(diagnostics[key]["autocorrelation"]))
        assert np.isfinite(diagnostics[key]["integrated_autocorrelation_time"])
    assert np.isfinite(diagnostics["summary"]["mean_acceptance_rate"])
