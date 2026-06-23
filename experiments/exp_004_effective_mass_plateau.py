"""Effective-mass plot from the toy glueball-like correlator."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rqm_yang_mills.correlators import temporal_correlator
from rqm_yang_mills.effective_mass import effective_mass


def main() -> None:
    output_data = ROOT / "outputs" / "data"
    output_figures = ROOT / "outputs" / "figures"
    output_data.mkdir(parents=True, exist_ok=True)
    output_figures.mkdir(parents=True, exist_ok=True)

    sample_path = output_data / "exp_003_glueball_samples.npy"
    if not sample_path.exists():
        raise SystemExit("Run exp_003_glueball_correlator.py before this script.")

    samples = np.load(sample_path)
    # The unconnected estimator is used for this tiny demonstration because the
    # connected estimator can change sign on very short exploratory chains.
    corr = temporal_correlator(samples, connected=False)
    mass = effective_mass(corr)

    np.savetxt(
        output_data / "exp_004_effective_mass_plateau.csv",
        np.column_stack([np.arange(mass.size), mass]),
        delimiter=",",
        header="t,m_eff",
        comments="",
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(np.arange(mass.size), mass, marker="o", linewidth=1.5)
    ax.set_xlabel("t")
    ax.set_ylabel("m_eff(t)")
    ax.set_title("Toy effective-mass estimator from unconnected C(t)")
    fig.tight_layout()
    fig.savefig(output_figures / "exp_004_effective_mass_plateau.png", dpi=160)

    print("effective-mass values:", mass)


if __name__ == "__main__":
    main()
