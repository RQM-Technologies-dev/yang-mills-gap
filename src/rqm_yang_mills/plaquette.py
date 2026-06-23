"""Plaquette and closure-defect computations."""

from __future__ import annotations

from itertools import combinations

import numpy as np
from numpy.typing import NDArray

from .gauge_field import GaugeField
from .lattice import Site
from .quaternions import inverse, multiply, scalar_part


def direction_pairs() -> tuple[tuple[int, int], ...]:
    return tuple(combinations(range(4), 2))


def spatial_direction_pairs() -> tuple[tuple[int, int], ...]:
    return tuple(combinations(range(3), 2))


def plaquette(field: GaugeField, site: Site, mu: int, nu: int) -> NDArray[np.float64]:
    """Compute ``U_mu(x) U_nu(x+mu) U_mu^-1(x+nu) U_nu^-1(x)``."""

    if mu == nu:
        raise ValueError("plaquette directions must be distinct")
    lattice = field.lattice
    x_plus_mu = lattice.shift(site, mu)
    x_plus_nu = lattice.shift(site, nu)
    return multiply(
        multiply(
            multiply(field.link(site, mu), field.link(x_plus_mu, nu)),
            inverse(field.link(x_plus_nu, mu)),
        ),
        inverse(field.link(site, nu)),
    )


def plaquette_scalar(field: GaugeField, site: Site, mu: int, nu: int) -> float:
    return float(scalar_part(plaquette(field, site, mu, nu)))


def closure_defect(field: GaugeField, site: Site, mu: int, nu: int) -> float:
    """Return ``D_p = 1 - scalar_part(U_p)`` for one plaquette."""

    return 1.0 - plaquette_scalar(field, site, mu, nu)


def all_plaquette_scalars(field: GaugeField) -> NDArray[np.float64]:
    scalars = np.empty(field.lattice.shape + (6,), dtype=float)
    for site in field.lattice.sites():
        for pair_index, (mu, nu) in enumerate(direction_pairs()):
            scalars[site + (pair_index,)] = plaquette_scalar(field, site, mu, nu)
    return scalars


def all_closure_defects(field: GaugeField) -> NDArray[np.float64]:
    return 1.0 - all_plaquette_scalars(field)
