import numpy as np

from yang_mills_gap.packet_analysis import load_config, load_diagnostics, load_observables, load_packet, summarize_packet
from yang_mills_gap.run_packet import (
    create_run_dir,
    save_array,
    save_diagnostics_json,
    save_manifest_json,
    save_records_csv,
)


def test_packet_analysis_reads_synthetic_packet(tmp_path) -> None:
    config = {"label": "synthetic packet", "claim_boundary": "diagnostic only"}
    run_dir = create_run_dir(tmp_path, "synthetic", config)
    save_records_csv(run_dir / "observables.csv", [{"sweep": 1.0, "action": 2.0}])
    save_diagnostics_json(run_dir / "diagnostics.json", {"summary": {"n_measurements": 1.0}})
    save_array(run_dir / "samples.npy", np.ones((2, 3)))
    save_manifest_json(
        run_dir,
        {
            "artifacts": {"observables": "observables.csv"},
            "arrays": {"samples": "samples.npy"},
        },
    )

    assert load_config(run_dir) == config
    assert load_observables(run_dir)[0]["action"] == 2
    assert load_diagnostics(run_dir)["summary"]["n_measurements"] == 1.0

    packet = load_packet(run_dir)
    assert np.array_equal(packet["arrays"]["samples"], np.ones((2, 3)))
    summary = summarize_packet(run_dir)
    assert summary["label"] == "synthetic packet"
    assert summary["n_observations"] == 1
    assert summary["arrays"]["samples"] == [2, 3]
