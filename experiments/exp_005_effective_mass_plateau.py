"""Effective-mass diagnostic from the connected correlator."""

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
from yang_mills_gap.effective_mass import effective_mass


def main() -> None:
    data_dir = ROOT / "outputs" / "data"
    fig_dir = ROOT / "outputs" / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    sample_path = data_dir / "exp_004_glueball_samples.npy"
    if not sample_path.exists():
        raise SystemExit("Run experiments/exp_004_glueball_correlator.py first.")

    samples = np.load(sample_path)
    corr = temporal_correlator(samples, connected=True)
    mass = effective_mass(corr)
    np.savetxt(
        data_dir / "exp_005_effective_mass_plateau.csv",
        np.column_stack([np.arange(mass.size), mass]),
        delimiter=",",
        header="t,m_eff",
        comments="",
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(np.arange(mass.size), mass, marker="o")
    ax.set_xlabel("t")
    ax.set_ylabel("m_eff(t)")
    ax.set_title("Effective-mass diagnostic")
    fig.tight_layout()
    fig.savefig(fig_dir / "exp_005_effective_mass_plateau.png", dpi=160)


if __name__ == "__main__":
    main()
