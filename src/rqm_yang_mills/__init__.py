"""Exploratory SU(2) lattice Yang-Mills tools in unit-quaternion coordinates.

The baseline modules implement standard SU(2) lattice Yang-Mills numerics.
RQM-inspired anchor or closure deformations are experimental and live outside
the baseline package unless explicitly marked otherwise.
"""

from .gauge_field import GaugeField
from .lattice import Lattice4D

__all__ = ["GaugeField", "Lattice4D"]
