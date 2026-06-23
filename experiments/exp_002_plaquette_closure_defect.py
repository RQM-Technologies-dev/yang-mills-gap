"""Plaquette closure-defect distributions for cold and random fields."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from yang_mills_gap.gauge_field import GaugeField
from yang_mills_gap.lattice import Lattice4D
from yang_mills_gap.plaquette import all_closure_defects


def main() -> None:
    data_dir = ROOT / "outputs" / "data"
    fig_dir = ROOT / "outputs" / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    lattice = Lattice4D((2, 2, 2, 2))
    rng = np.random.default_rng(2002)
    cold = all_closure_defects(GaugeField.cold(lattice)).ravel()
    random = all_closure_defects(GaugeField.random(lattice, rng)).ravel()

    np.savetxt(
        data_dir / "exp_002_plaquette_closure_defect.csv",
        np.column_stack([cold, random]),
        delimiter=",",
        header="cold,random",
        comments="",
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(random, bins=24, alpha=0.75, label="random field")
    ax.axvline(float(np.max(np.abs(cold))), color="black", linestyle="--", label="cold max")
    ax.set_xlabel("D_p = 1 - scalar_part(U_p)")
    ax.set_ylabel("count")
    ax.set_title("Plaquette closure defect")
    ax.legend()
    fig.tight_layout()
    fig.savefig(fig_dir / "exp_002_plaquette_closure_defect.png", dpi=160)


if __name__ == "__main__":
    main()
