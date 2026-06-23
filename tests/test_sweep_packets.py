import pytest

from yang_mills_gap.sweep_packets import build_sweep_config, make_sweep_summary_record


def test_build_sweep_config_is_serializable_and_carries_claim_boundary() -> None:
    config = build_sweep_config(
        betas=[1.8],
        seeds=[101],
        lattice_shape=(1, 1, 1, 4),
        n_sweeps=4,
        thermalization=1,
        measure_every=1,
        step_size=0.2,
        n_bootstrap=3,
    )

    assert config["betas"] == [1.8]
    assert config["seeds"] == [101]
    assert config["baseline"] == "standard SU(2) Wilson action only"
    assert "closure-resonance" in config["research_objective"]
    assert "diagnostic" in config["claim_boundary"]


def test_make_sweep_summary_record() -> None:
    record = make_sweep_summary_record(
        2.2,
        101,
        "packet-dir",
        {
            "mean_acceptance_rate": 0.9,
            "final_average_plaquette": 0.2,
            "final_average_closure_defect": 0.8,
            "n_measurements": 3,
            "research_objective": "objective",
            "claim_boundary": "boundary",
        },
    )

    assert record["beta"] == 2.2
    assert record["seed"] == 101
    assert record["packet_dir"] == "packet-dir"
    assert record["claim_boundary"] == "boundary"


def test_build_sweep_config_validates_basic_inputs() -> None:
    with pytest.raises(ValueError, match="betas"):
        build_sweep_config(
            betas=[],
            seeds=[101],
            lattice_shape=(1, 1, 1, 4),
            n_sweeps=4,
            thermalization=1,
            measure_every=1,
            step_size=0.2,
        )

    with pytest.raises(ValueError, match="measure_every"):
        build_sweep_config(
            betas=[1.8],
            seeds=[101],
            lattice_shape=(1, 1, 1, 4),
            n_sweeps=4,
            thermalization=1,
            measure_every=0,
            step_size=0.2,
        )
