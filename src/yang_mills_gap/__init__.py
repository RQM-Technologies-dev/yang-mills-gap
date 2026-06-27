"""Finite-lattice SU(2) Wilson-action tools for the proof program.

The baseline modules support curvature-closure proof scaffolding. They do not
claim a continuum Yang-Mills construction or a completed mass-gap proof.
"""

from .gauge_field import GaugeField
from .lattice import Lattice4D

__all__ = ["GaugeField", "Lattice4D"]
