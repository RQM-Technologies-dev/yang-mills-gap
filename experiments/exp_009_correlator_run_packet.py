"""Create a tiny correlator/effective-mass diagnostic run packet.

This baseline Wilson-action packet is diagnostic only. It is not a Clay
mass-gap result and does not use the nonstandard RQM anchor deformation.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from yang_mills_gap.gauge_field import GaugeField
from yang_mills_gap.lattice import Lattice4D
from yang_mills_gap.monte_carlo import metropolis_sweep_local
from yang_mills_gap.observables import average_closure_defect, average_plaquette, glueball_timeseries
from yang_mills_gap.run_packet import create_run_dir
from yang_mills_gap.spectroscopy_packet import write_correlator_packet
from yang_mills_gap.wilson_action import wilson_action


def main() -> None:
    config = {
        "label": "tiny finite-lattice correlator/effective-mass sanity diagnostic",
        "research_objective": "build auditable finite-lattice diagnostics for the closure-resonance working hypothesis",
        "lattice_shape": (1, 1, 1, 4),
        "beta": 2.2,
        "n_sweeps": 18,
        "step_size": 0.42,
        "thermalization": 4,
        "measure_every": 1,
        "hot_start": False,
        "use_local_action": True,
        "seed": 9009,
        "n_bootstrap": 100,
        "mean_mode": "global",
        "claim_boundary": "diagnostic packet only; not a mass-gap estimate",
    }
    run_dir = create_run_dir(ROOT / "outputs" / "run_packets", "exp_009_correlator_run_packet", config)
    rng = np.random.default_rng(int(config["seed"]))
    lattice = Lattice4D(tuple(config["lattice_shape"]))
    field = GaugeField.random(lattice, rng) if config["hot_start"] else GaugeField.cold(lattice)
    records: list[dict[str, float]] = []
    samples: list[np.ndarray] = []
    for sweep in range(1, int(config["n_sweeps"]) + 1):
        stats = metropolis_sweep_local(field, float(config["beta"]), step_size=float(config["step_size"]), rng=rng)
        if sweep > int(config["thermalization"]) and (sweep - int(config["thermalization"])) % int(config["measure_every"]) == 0:
            records.append(
                {
                    "sweep": float(sweep),
                    "action": wilson_action(field, float(config["beta"])),
                    "average_plaquette": average_plaquette(field),
                    "average_closure_defect": average_closure_defect(field),
                    "acceptance_rate": stats.acceptance_rate,
                }
            )
            samples.append(glueball_timeseries(field))

    packet_dir = write_correlator_packet(
        run_dir,
        config,
        records,
        np.vstack(samples),
        n_bootstrap=int(config["n_bootstrap"]),
        seed=int(config["seed"]) + 1,
        mean_mode=str(config["mean_mode"]),
    )
    print(f"Wrote correlator diagnostic run packet: {packet_dir}")


if __name__ == "__main__":
    main()
