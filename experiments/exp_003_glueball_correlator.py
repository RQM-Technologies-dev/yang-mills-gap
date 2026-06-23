"""Toy glueball-like correlator from spatial plaquette operators."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rqm_yang_mills.gauge_field import GaugeField
from rqm_yang_mills.lattice import Lattice4D
from rqm_yang_mills.monte_carlo import metropolis_sweep
from rqm_yang_mills.observables import glueball_timeseries
from rqm_yang_mills.correlators import temporal_correlator


def main() -> None:
    output_data = ROOT / "outputs" / "data"
    output_figures = ROOT / "outputs" / "figures"
    output_data.mkdir(parents=True, exist_ok=True)
    output_figures.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(3003)
    lattice = Lattice4D((1, 1, 1, 4))
    field = GaugeField.cold(lattice)
    samples: list[np.ndarray] = []

    for sweep in range(1, 13):
        metropolis_sweep(field, beta=2.2, step_size=0.42, rng=rng)
        if sweep > 4:
            samples.append(glueball_timeseries(field))

    sample_array = np.vstack(samples)
    connected = temporal_correlator(sample_array, connected=True)
    unconnected = temporal_correlator(sample_array, connected=False)

    np.save(output_data / "exp_003_glueball_samples.npy", sample_array)
    np.savetxt(
        output_data / "exp_003_glueball_correlator.csv",
        np.column_stack([np.arange(connected.size), connected, unconnected]),
        delimiter=",",
        header="dt,connected,unconnected",
        comments="",
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(np.arange(connected.size), connected, marker="o", label="connected")
    ax.plot(np.arange(unconnected.size), unconnected, marker="s", label="unconnected")
    ax.set_xlabel("temporal separation dt")
    ax.set_ylabel("C(dt)")
    ax.set_title("Glueball-like spatial-plaquette correlator")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_figures / "exp_003_glueball_correlator.png", dpi=160)

    print(f"collected {sample_array.shape[0]} samples with Nt={sample_array.shape[1]}")


if __name__ == "__main__":
    main()
