import importlib.util
from pathlib import Path

from yang_mills_gap.run_packet import create_run_dir, save_diagnostics_json, save_records_csv


def load_inspector_module():
    path = Path(__file__).resolve().parents[1] / "experiments" / "inspect_latest_packet.py"
    spec = importlib.util.spec_from_file_location("inspect_latest_packet", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_find_latest_packet_and_read_first_rows(tmp_path) -> None:
    module = load_inspector_module()
    older = create_run_dir(tmp_path, "older", {"label": "older"})
    save_records_csv(older / "observables.csv", [{"sweep": 1.0}])
    save_diagnostics_json(older / "diagnostics.json", {"summary": {}})
    newer = create_run_dir(tmp_path, "newer", {"label": "newer"})
    save_records_csv(newer / "observables.csv", [{"sweep": 2.0}])
    save_diagnostics_json(newer / "diagnostics.json", {"summary": {}})

    latest = module.find_latest_packet(tmp_path)
    assert latest.name.endswith("newer")
    assert module.read_first_rows(newer / "observables.csv")[0]["sweep"] == "2.0"
