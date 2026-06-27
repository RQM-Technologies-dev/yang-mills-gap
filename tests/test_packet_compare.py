import csv
import json

import numpy as np

from yang_mills_gap.packet_compare import (
    compare_packet_summaries,
    load_sweep_summary,
    save_packet_comparison_csv,
    summarize_effective_mass_packet,
)
from yang_mills_gap.run_packet import create_run_dir, save_diagnostics_json, save_manifest_json, save_records_csv


def make_minimal_effective_mass_packet(tmp_path):
    config = {
        "label": "minimal packet",
        "research_objective": "compare diagnostics",
        "claim_boundary": "diagnostic only",
        "beta": 2.2,
        "lattice_shape": [1, 1, 1, 4],
    }
    run_dir = create_run_dir(tmp_path, "packet", config)
    save_records_csv(
        run_dir / "observables.csv",
        [{"sweep": 1.0, "average_plaquette": 0.2, "average_closure_defect": 0.8, "acceptance_rate": 0.9}],
    )
    save_diagnostics_json(
        run_dir / "diagnostics.json",
        {"summary": {"n_measurements": 1.0, "mean_acceptance_rate": 0.9}},
    )
    save_records_csv(
        run_dir / "effective_mass.csv",
        [
            {"t": 0.0, "m_eff_log": "", "m_eff_cosh": "nan"},
            {"t": 1.0, "m_eff_log": 0.7, "m_eff_cosh": 0.5},
            {"t": 2.0, "m_eff_log": 0.72, "m_eff_cosh": 0.52},
            {"t": 3.0, "m_eff_log": 0.69, "m_eff_cosh": 0.51},
        ],
    )
    save_records_csv(
        run_dir / "correlator.csv",
        [
            {"t": 0.0, "connected_correlator": 1.0, "bootstrap_stderr": 0.1},
            {"t": 1.0, "connected_correlator": -0.5, "bootstrap_stderr": 0.2},
            {"t": 2.0, "connected_correlator": 0.25, "bootstrap_stderr": ""},
        ],
    )
    save_manifest_json(run_dir, {"artifacts": {"effective_mass": "effective_mass.csv"}})
    (run_dir / "quality_gates.json").write_text(
        json.dumps(
            {
                "summary": {
                    "interpretation_status": "diagnostic_with_warnings",
                    "n_fail": 0,
                    "n_warn": 1,
                },
                "gates": [],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (run_dir / "candidate_assessment.json").write_text(
        json.dumps(
            {
                "candidate_status": "candidate_with_warnings",
                "selected_estimator": "cosh",
                "candidate_mean": 0.51,
                "candidate_relative_std": 0.02,
            }
        )
        + "\n",
        encoding="utf-8",
    )
    return run_dir


def make_invalid_effective_mass_packet(tmp_path):
    config = {
        "label": "invalid packet",
        "research_objective": "compare diagnostics",
        "claim_boundary": "diagnostic only",
        "beta": 2.0,
        "lattice_shape": [1, 1, 1, 4],
    }
    run_dir = create_run_dir(tmp_path, "invalid-packet", config)
    save_records_csv(
        run_dir / "observables.csv",
        [{"sweep": 1.0, "average_plaquette": 0.2, "average_closure_defect": 0.8, "acceptance_rate": 0.9}],
    )
    save_diagnostics_json(run_dir / "diagnostics.json", {"summary": {"n_measurements": 1.0}})
    save_records_csv(
        run_dir / "effective_mass.csv",
        [
            {"t": 0.0, "m_eff_log": "", "m_eff_cosh": "nan"},
            {"t": 1.0, "m_eff_log": "inf", "m_eff_cosh": ""},
        ],
    )
    save_records_csv(
        run_dir / "correlator.csv",
        [
            {"t": 0.0, "connected_correlator": "", "bootstrap_stderr": ""},
            {"t": 1.0, "connected_correlator": "nan", "bootstrap_stderr": "inf"},
        ],
    )
    save_manifest_json(run_dir, {"artifacts": {"effective_mass": "effective_mass.csv"}})
    return run_dir


def test_summarize_effective_mass_packet_handles_finite_and_invalid_values(tmp_path) -> None:
    run_dir = make_minimal_effective_mass_packet(tmp_path)
    summary = summarize_effective_mass_packet(run_dir)

    assert summary["research_objective"] == "compare diagnostics"
    assert summary["claim_boundary"] == "diagnostic only"
    assert summary["quality_gate_status"] == "diagnostic_with_warnings"
    assert summary["quality_gate_fail_count"] == 0
    assert summary["quality_gate_warn_count"] == 1
    assert summary["candidate_status"] == "candidate_with_warnings"
    assert summary["candidate_estimator"] == "cosh"
    assert summary["candidate_mean"] == 0.51
    assert summary["min_finite_m_eff_log"] == 0.69
    assert summary["min_finite_m_eff_cosh"] == 0.5
    assert summary["n_finite_m_eff_log"] == 3
    assert summary["n_finite_m_eff_cosh"] == 3
    assert summary["first_finite_m_eff_log"] == 0.7
    assert summary["median_finite_m_eff_cosh"] == 0.51
    assert summary["mean_finite_m_eff_log"] == np.mean([0.7, 0.72, 0.69])
    assert summary["correlator_positive_count"] == 2
    assert summary["correlator_negative_count"] == 1
    assert summary["correlator_sign_change_count"] == 2
    assert summary["correlator_abs_mean"] == np.mean([1.0, 0.5, 0.25])
    assert summary["correlator_noise_proxy_mean_stderr"] == 0.15000000000000002
    assert summary["n_log_plateau_candidates"] > 0
    assert summary["n_cosh_plateau_candidates"] > 0
    assert summary["best_cosh_plateau_mean"] != ""
    assert summary["best_cosh_plateau_relative_std"] != ""


def test_summarize_effective_mass_packet_handles_no_finite_effective_masses(tmp_path) -> None:
    run_dir = make_invalid_effective_mass_packet(tmp_path)
    summary = summarize_effective_mass_packet(run_dir)

    assert summary["min_finite_m_eff_log"] == ""
    assert summary["min_finite_m_eff_cosh"] == ""
    assert summary["n_finite_m_eff_log"] == 0
    assert summary["n_finite_m_eff_cosh"] == 0
    assert summary["first_finite_m_eff_log"] == ""
    assert summary["median_finite_m_eff_cosh"] == ""
    assert summary["mean_finite_m_eff_log"] == ""
    assert summary["correlator_positive_count"] == 0
    assert summary["correlator_negative_count"] == 0
    assert summary["correlator_sign_change_count"] == 0
    assert summary["correlator_abs_mean"] == ""
    assert summary["correlator_noise_proxy_mean_stderr"] == ""
    assert summary["n_log_plateau_candidates"] == 0
    assert summary["best_log_plateau_mean"] == ""


def test_save_packet_comparison_csv_and_load_sweep_summary(tmp_path) -> None:
    run_dir = make_minimal_effective_mass_packet(tmp_path)
    summaries = compare_packet_summaries([run_dir])
    comparison_path = save_packet_comparison_csv(tmp_path / "comparison.csv", summaries)
    sweep_path = tmp_path / "sweep_summary.csv"
    save_records_csv(sweep_path, [{"beta": 2.2, "packet_dir": str(run_dir)}])

    with comparison_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert rows[0]["label"] == "minimal packet"
    assert load_sweep_summary(tmp_path)[0]["beta"] == "2.2"
