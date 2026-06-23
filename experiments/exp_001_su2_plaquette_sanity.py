"""Sanity checks for SU(2) plaquettes in quaternion coordinates."""

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
from rqm_yang_mills.plaquette import all_closure_defects


def main() -> None:
    output_data = ROOT / "outputs" / "data"
    output_figures = ROOT / "outputs" / "figures"
    output_data.mkdir(parents=True, exist_ok=True)
    output_figures.mkdir(parents=True, exist_ok=True)

    lattice = Lattice4D((2, 2, 2, 2))
    cold = GaugeField.cold(lattice)
    rng = np.random.default_rng(1001)
    hot = GaugeField.random(lattice, rng)

    cold_defects = all_closure_defects(cold).ravel()
    hot_defects = all_closure_defects(hot).ravel()

    np.savetxt(output_data / "exp_001_cold_closure_defects.csv", cold_defects, delimiter=",")
    np.savetxt(output_data / "exp_001_hot_closure_defects.csv", hot_defects, delimiter=",")

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(hot_defects, bins=24, alpha=0.8, label="random links")
    ax.axvline(float(np.max(np.abs(cold_defects))), color="black", linestyle="--", label="cold max")
    ax.set_xlabel("closure defect D_p = 1 - scalar(U_p)")
    ax.set_ylabel("count")
    ax.set_title("SU(2) plaquette closure-defect sanity check")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_figures / "exp_001_su2_plaquette_sanity.png", dpi=160)

    print(f"cold max defect: {np.max(np.abs(cold_defects)):.3e}")
    print(f"hot mean defect: {np.mean(hot_defects):.6f}")


if __name__ == "__main__":
    main()
