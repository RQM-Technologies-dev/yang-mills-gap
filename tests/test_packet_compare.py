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
        ],
    )
    save_manifest_json(run_dir, {"artifacts": {"effective_mass": "effective_mass.csv"}})
    return run_dir


def test_summarize_effective_mass_packet_handles_finite_and_invalid_values(tmp_path) -> None:
    run_dir = make_minimal_effective_mass_packet(tmp_path)
    summary = summarize_effective_mass_packet(run_dir)

    assert summary["research_objective"] == "compare diagnostics"
    assert summary["claim_boundary"] == "diagnostic only"
    assert summary["min_finite_m_eff_log"] == 0.7
    assert summary["min_finite_m_eff_cosh"] == 0.5
    assert summary["n_finite_m_eff_log"] == 1
    assert summary["n_finite_m_eff_cosh"] == 1


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
