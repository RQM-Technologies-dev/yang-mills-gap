"""Wilson action for the SU(2) quaternion lattice representation."""

from __future__ import annotations

import numpy as np

from .gauge_field import GaugeField
from .plaquette import all_closure_defects


def wilson_action(field: GaugeField, beta: float) -> float:
    """Return ``S = beta * sum_p (1 - scalar_part(U_p))``."""

    if beta < 0:
        raise ValueError("beta must be nonnegative")
    return float(beta * np.sum(all_closure_defects(field)))
