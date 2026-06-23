import importlib.util
from pathlib import Path

from yang_mills_gap.run_packet import save_records_csv


def load_sweep_inspector_module():
    path = Path(__file__).resolve().parents[1] / "experiments" / "inspect_latest_sweep.py"
    spec = importlib.util.spec_from_file_location("inspect_latest_sweep", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_find_latest_sweep_and_summary_helpers(tmp_path) -> None:
    module = load_sweep_inspector_module()
    older = tmp_path / "20260101T000000Z-old"
    newer = tmp_path / "20260102T000000Z-new"
    older.mkdir()
    newer.mkdir()
    save_records_csv(older / "packet_comparison.csv", [{"beta": 1.8, "best_cosh_plateau_relative_std": 0.2}])
    save_records_csv(newer / "packet_comparison.csv", [{"beta": 2.0, "best_cosh_plateau_relative_std": 0.1}])
    save_records_csv(newer / "sweep_summary.csv", [{"beta": 2.0, "seed": 101}, {"beta": 2.0, "seed": 202}])

    latest = module.find_latest_sweep(tmp_path)
    rows = module.load_csv_rows(latest / "sweep_summary.csv")
    comparison = module.load_csv_rows(latest / "packet_comparison.csv")

    assert latest == newer
    assert module.unique_values(rows, "seed") == ["101", "202"]
    assert module.best_packet_by_cosh_plateau(comparison)["beta"] == "2.0"
    assert module.has_plateau_candidates([{"n_log_plateau_candidates": "0", "n_cosh_plateau_candidates": "1"}])
    assert not module.has_plateau_candidates([{"n_log_plateau_candidates": "0", "n_cosh_plateau_candidates": ""}])
