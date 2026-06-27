import pytest

from yang_mills_gap.baseline_contract import (
    BASELINE_CLAIM_BOUNDARY,
    BASELINE_NAME,
    BASELINE_RESEARCH_OBJECTIVE,
    baseline_metadata,
    validate_baseline_sweep_config,
)
from yang_mills_gap.sweep_packets import build_sweep_config


def test_baseline_metadata_carries_standard_wilson_contract() -> None:
    metadata = baseline_metadata(glueball_operator="spatial_wilson_loops")

    assert metadata["baseline"] == BASELINE_NAME
    assert metadata["claim_boundary"] == BASELINE_CLAIM_BOUNDARY
    assert metadata["research_objective"] == BASELINE_RESEARCH_OBJECTIVE
    assert metadata["glueball_operator"] == "spatial_wilson_loops"
    assert "no anchor or deformation term" in metadata["baseline_dynamics"]


def test_baseline_metadata_rejects_nonbaseline_operator() -> None:
    with pytest.raises(ValueError, match="glueball_operator"):
        baseline_metadata(glueball_operator="anchor_deformed")


def test_baseline_sweep_config_rejects_deformation_keys() -> None:
    config = build_sweep_config(
        betas=[1.8],
        seeds=[101],
        lattice_shape=(1, 1, 1, 4),
        n_sweeps=4,
        thermalization=1,
        measure_every=1,
        step_size=0.2,
    )
    config["anchor_strength"] = 0.8

    with pytest.raises(ValueError, match="nonstandard deformation"):
        validate_baseline_sweep_config(config)


def test_build_sweep_config_rejects_nonlocal_baseline_sweeps() -> None:
    with pytest.raises(ValueError, match="use_local_action=True"):
        build_sweep_config(
            betas=[1.8],
            seeds=[101],
            lattice_shape=(1, 1, 1, 4),
            n_sweeps=4,
            thermalization=1,
            measure_every=1,
            step_size=0.2,
            use_local_action=False,
        )
