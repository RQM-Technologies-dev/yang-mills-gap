import importlib.util
from pathlib import Path

import numpy as np


def load_exp_009_module():
    path = Path(__file__).resolve().parents[1] / "experiments" / "exp_009_correlator_run_packet.py"
    spec = importlib.util.spec_from_file_location("exp_009_correlator_run_packet", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exp_009_correlator_helpers_produce_expected_arrays_on_synthetic_data() -> None:
    module = load_exp_009_module()
    base = np.array([1.0, 0.8, 0.6, 0.8])
    samples = np.vstack([base + 0.02 * index for index in range(6)])
    artifacts = module.compute_correlator_artifacts(samples, n_bootstrap=5, seed=123)

    assert artifacts["correlator"].shape == (4,)
    assert artifacts["correlator_stderr"].shape == (4,)
    assert artifacts["effective_mass_log"].shape == (3,)
    assert artifacts["effective_mass_cosh"].shape == (4,)
    assert np.all(np.isfinite(artifacts["correlator"]))
    assert np.all(np.isfinite(artifacts["correlator_stderr"]))
