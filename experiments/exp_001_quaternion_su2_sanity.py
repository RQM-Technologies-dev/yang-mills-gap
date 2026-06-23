"""Quaternion SU(2) sanity checks."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from yang_mills_gap.quaternions import inverse, multiply, norm, random_unit_quaternion


def main() -> None:
    data_dir = ROOT / "outputs" / "data"
    fig_dir = ROOT / "outputs" / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(1001)
    q = random_unit_quaternion(rng, shape=(1024,))
    products = multiply(q, inverse(q))
    deviations = np.linalg.norm(products - np.array([1.0, 0.0, 0.0, 0.0]), axis=-1)

    np.savetxt(
        data_dir / "exp_001_quaternion_su2_sanity.csv",
        np.column_stack([norm(q), deviations]),
        delimiter=",",
        header="norm,identity_deviation",
        comments="",
    )

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].hist(norm(q), bins=24)
    axes[0].set_xlabel("||q||")
    axes[0].set_ylabel("count")
    axes[0].set_title("Unit quaternion norms")
    axes[1].hist(deviations, bins=24)
    axes[1].set_xlabel("||q q^-1 - 1||")
    axes[1].set_title("Inverse identity deviation")
    fig.tight_layout()
    fig.savefig(fig_dir / "exp_001_quaternion_su2_sanity.png", dpi=160)


if __name__ == "__main__":
    main()
