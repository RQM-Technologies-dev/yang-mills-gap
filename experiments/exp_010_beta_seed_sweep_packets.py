"""Create a tiny beta/seed sweep of correlator/effective-mass packets.

This is an artifact-driven finite-lattice diagnostic sweep for the standard
SU(2) Wilson-action baseline. It is not a continuum result or mass-gap estimate.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from yang_mills_gap.sweep_packets import build_sweep_config, create_sweep_dir, run_beta_seed_sweep


def main() -> None:
    config = build_sweep_config(
        betas=[1.8, 2.0, 2.2, 2.4],
        seeds=[101, 202, 303],
        lattice_shape=(1, 1, 1, 4),
        n_sweeps=18,
        thermalization=4,
        measure_every=1,
        step_size=0.42,
        use_local_action=True,
        hot_start=False,
        n_bootstrap=100,
        mean_mode="global",
    )
    sweep_dir = create_sweep_dir(ROOT / "outputs" / "run_packets" / "sweeps", "exp_010_beta_seed_sweep")
    result = run_beta_seed_sweep(sweep_dir, config)
    print(f"Wrote beta/seed diagnostic sweep: {result['sweep_dir']}")
    print(f"Packets: {len(result['packet_dirs'])}")


if __name__ == "__main__":
    main()
