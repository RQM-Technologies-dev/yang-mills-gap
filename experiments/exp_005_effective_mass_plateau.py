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
from yang_mills_gap.effective_mass import effective_mass, effective_mass_cosh


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
    mass_log = effective_mass(corr)
    mass_cosh = effective_mass_cosh(corr)
    padded_log = np.full_like(mass_cosh, np.nan)
    padded_log[: mass_log.size] = mass_log
    np.savetxt(
        data_dir / "exp_005_effective_mass_plateau.csv",
        np.column_stack([np.arange(mass_cosh.size), padded_log, mass_cosh]),
        delimiter=",",
        header="t,m_eff_log,m_eff_cosh",
        comments="",
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(np.arange(padded_log.size), padded_log, marker="o", label="log")
    ax.plot(np.arange(mass_cosh.size), mass_cosh, marker="s", label="cosh")
    ax.set_xlabel("t")
    ax.set_ylabel("m_eff(t)")
    ax.set_title("Effective-mass diagnostic")
    ax.legend()
    fig.tight_layout()
    fig.savefig(fig_dir / "exp_005_effective_mass_plateau.png", dpi=160)


if __name__ == "__main__":
    main()
