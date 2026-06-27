"""Modest larger finite-lattice spectroscopy packet sweep.

This experiment remains a standard SU(2) Wilson-action finite-lattice
diagnostic. It uses local Metropolis updates and an improved gauge-invariant
measurement operator built from small spatial Wilson loops. It is not a
continuum result or mass-gap estimate.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from yang_mills_gap.sweep_packets import build_sweep_config, create_sweep_dir, run_beta_seed_sweep


LATTICE_SHAPE = (2, 2, 2, 4)
BETAS = [2.0, 2.4]
SEEDS = [401, 502]
N_SWEEPS = 12
THERMALIZATION = 3
MEASURE_EVERY = 1
STEP_SIZE = 0.32
HOT_START = False
N_BOOTSTRAP = 60
MEAN_MODE = "global"
GLUEBALL_OPERATOR = "spatial_wilson_loops"


def main() -> None:
    config = build_sweep_config(
        betas=BETAS,
        seeds=SEEDS,
        lattice_shape=LATTICE_SHAPE,
        n_sweeps=N_SWEEPS,
        thermalization=THERMALIZATION,
        measure_every=MEASURE_EVERY,
        step_size=STEP_SIZE,
        use_local_action=True,
        hot_start=HOT_START,
        n_bootstrap=N_BOOTSTRAP,
        mean_mode=MEAN_MODE,
        glueball_operator=GLUEBALL_OPERATOR,
    )
    config["label"] = "modest larger finite-lattice spectroscopy sweep"
    config["operator_note"] = "standard Wilson-action baseline measured with spatial 1x1, 1x2, and 2x1 Wilson-loop operator"

    sweep_dir = create_sweep_dir(ROOT / "outputs" / "run_packets" / "sweeps", "exp_011_larger_spectroscopy_sweep")
    result = run_beta_seed_sweep(sweep_dir, config)
    print(f"Wrote larger spectroscopy diagnostic sweep: {result['sweep_dir']}")
    print(f"Packets: {len(result['packet_dirs'])}")
    print(f"Glueball operator: {GLUEBALL_OPERATOR}")


if __name__ == "__main__":
    main()
