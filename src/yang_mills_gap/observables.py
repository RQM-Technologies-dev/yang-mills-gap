"""Gauge-invariant observables for small exploratory lattice runs."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from .gauge_field import GaugeField
from .lattice import Site
from .plaquette import all_closure_defects, all_plaquette_scalars, plaquette_scalar, spatial_direction_pairs
from .quaternions import IDENTITY, inverse, multiply, scalar_part


def average_plaquette(field: GaugeField) -> float:
    """Mean scalar part of all oriented ``mu < nu`` plaquettes."""

    return float(np.mean(all_plaquette_scalars(field)))


def average_closure_defect(field: GaugeField) -> float:
    """Mean ``D_p = 1 - scalar_part(U_p)`` over all oriented ``mu < nu`` plaquettes."""

    return float(np.mean(all_closure_defects(field)))


def wilson_loop_scalar(
    field: GaugeField,
    origin: Site,
    mu: int,
    nu: int,
    extent_mu: int,
    extent_nu: int,
) -> float:
    """Scalar part of a rectangular Wilson loop in the ``mu``-``nu`` plane."""

    if mu == nu:
        raise ValueError("Wilson loop directions must be distinct")
    if extent_mu <= 0 or extent_nu <= 0:
        raise ValueError("Wilson loop extents must be positive")

    lattice = field.lattice
    site = origin
    loop = IDENTITY.copy()

    for _ in range(extent_mu):
        loop = multiply(loop, field.link(site, mu))
        site = lattice.shift(site, mu)
    for _ in range(extent_nu):
        loop = multiply(loop, field.link(site, nu))
        site = lattice.shift(site, nu)
    for _ in range(extent_mu):
        site = lattice.shift(site, mu, step=-1)
        loop = multiply(loop, inverse(field.link(site, mu)))
    for _ in range(extent_nu):
        site = lattice.shift(site, nu, step=-1)
        loop = multiply(loop, inverse(field.link(site, nu)))

    return float(scalar_part(loop))


def glueball_operator(field: GaugeField, t: int) -> float:
    """A simple scalar glueball-like operator from spatial plaquettes at time ``t``."""

    lattice = field.lattice
    t_mod = t % lattice.shape[3]
    values: list[float] = []
    for x in range(lattice.shape[0]):
        for y in range(lattice.shape[1]):
            for z in range(lattice.shape[2]):
                site = (x, y, z, t_mod)
                for mu, nu in spatial_direction_pairs():
                    values.append(plaquette_scalar(field, site, mu, nu))
    return float(np.mean(values))


def glueball_timeseries(field: GaugeField) -> NDArray[np.float64]:
    """Return ``O(t)`` for every temporal slice."""

    return np.array(
        [glueball_operator(field, t) for t in range(field.lattice.shape[3])],
        dtype=float,
    )
