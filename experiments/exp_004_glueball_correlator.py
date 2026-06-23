"""Glueball-like connected correlator from spatial plaquettes."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from yang_mills_gap.correlators import temporal_correlator
from yang_mills_gap.gauge_field import GaugeField
from yang_mills_gap.lattice import Lattice4D
from yang_mills_gap.monte_carlo import metropolis_sweep
from yang_mills_gap.observables import glueball_timeseries


def main() -> None:
    data_dir = ROOT / "outputs" / "data"
    fig_dir = ROOT / "outputs" / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(4004)
    field = GaugeField.cold(Lattice4D((1, 1, 1, 4)))
    samples: list[np.ndarray] = []
    for sweep in range(1, 13):
        metropolis_sweep(field, beta=2.2, step_size=0.42, rng=rng)
        if sweep > 4:
            samples.append(glueball_timeseries(field))

    sample_array = np.vstack(samples)
    connected = temporal_correlator(sample_array, connected=True)
    np.save(data_dir / "exp_004_glueball_samples.npy", sample_array)
    np.savetxt(
        data_dir / "exp_004_glueball_correlator.csv",
        np.column_stack([np.arange(connected.size), connected]),
        delimiter=",",
        header="dt,connected_C",
        comments="",
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(np.arange(connected.size), connected, marker="o")
    ax.set_xlabel("temporal separation dt")
    ax.set_ylabel("connected C(dt)")
    ax.set_title("Glueball-like connected correlator")
    fig.tight_layout()
    fig.savefig(fig_dir / "exp_004_glueball_correlator.png", dpi=160)


if __name__ == "__main__":
    main()
