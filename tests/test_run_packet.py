import csv
import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from yang_mills_gap.run_packet import (
    create_run_dir,
    save_array,
    save_diagnostics_json,
    save_figure,
    save_manifest_json,
    save_records_csv,
)


def test_run_packet_creates_expected_files(tmp_path) -> None:
    config = {"beta": 2.2, "label": "tiny sanity diagnostic"}
    run_dir = create_run_dir(tmp_path, "packet-test", config)
    records_path = save_records_csv(
        run_dir / "observables.csv",
        [{"sweep": 1.0, "action": 2.0}, {"sweep": 2.0, "action": 1.5}],
    )
    diagnostics_path = save_diagnostics_json(run_dir / "diagnostics.json", {"action": {"iat": 0.5}})

    fig, ax = plt.subplots()
    ax.plot([0, 1], [1, 0])
    figure_path = save_figure(run_dir, fig, "example.png")
    plt.close(fig)

    assert run_dir.exists()
    assert json.loads((run_dir / "config.json").read_text()) == config
    with records_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert rows[0]["sweep"] == "1.0"
    assert json.loads(diagnostics_path.read_text()) == {"action": {"iat": 0.5}}
    assert figure_path == run_dir / "plots" / "example.png"
    assert figure_path.exists()


def test_manifest_and_array_writers(tmp_path) -> None:
    run_dir = create_run_dir(tmp_path, "manifest-test", {"label": "diagnostic"})
    array_path = save_array(run_dir / "samples.npy", np.arange(6).reshape(2, 3))
    manifest_path = save_manifest_json(
        run_dir,
        {
            "artifacts": {"samples": "samples.npy"},
            "arrays": {"samples": "samples.npy"},
        },
    )

    assert array_path == run_dir / "samples.npy"
    assert np.array_equal(np.load(array_path), np.arange(6).reshape(2, 3))
    assert json.loads(manifest_path.read_text())["arrays"]["samples"] == "samples.npy"
