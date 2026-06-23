"""Closure-defect histograms before and after baseline Wilson-action updates."""

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
from rqm_yang_mills.plaquette import all_closure_defects


def main() -> None:
    output_data = ROOT / "outputs" / "data"
    output_figures = ROOT / "outputs" / "figures"
    output_data.mkdir(parents=True, exist_ok=True)
    output_figures.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(5005)
    lattice = Lattice4D((2, 2, 2, 2))
    field = GaugeField.random(lattice, rng)
    initial = all_closure_defects(field).ravel()

    for _ in range(8):
        metropolis_sweep(field, beta=2.2, step_size=0.40, rng=rng)

    evolved = all_closure_defects(field).ravel()
    np.savetxt(
        output_data / "exp_005_closure_defect_histograms.csv",
        np.column_stack([initial, evolved]),
        delimiter=",",
        header="initial,evolved",
        comments="",
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    bins = np.linspace(0.0, 2.0, 32)
    ax.hist(initial, bins=bins, alpha=0.55, label="initial random")
    ax.hist(evolved, bins=bins, alpha=0.65, label="after baseline updates")
    ax.set_xlabel("closure defect D_p")
    ax.set_ylabel("count")
    ax.set_title("Closure-defect distribution under standard Wilson updates")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_figures / "exp_005_closure_defect_histograms.png", dpi=160)

    print(f"initial mean defect: {np.mean(initial):.6f}")
    print(f"evolved mean defect: {np.mean(evolved):.6f}")


if __name__ == "__main__":
    main()
