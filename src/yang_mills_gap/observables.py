"""Gauge-invariant observables for small exploratory lattice runs."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from .gauge_field import GaugeField
from .lattice import Site
from .plaquette import all_closure_defects, all_plaquette_scalars, plaquette_scalar, spatial_direction_pairs
from .quaternions import IDENTITY, inverse, multiply, scalar_part

GLUEBALL_OPERATOR_SPATIAL_PLAQUETTE = "spatial_plaquette"
GLUEBALL_OPERATOR_SPATIAL_WILSON_LOOPS = "spatial_wilson_loops"
GLUEBALL_OPERATOR_MODES = (
    GLUEBALL_OPERATOR_SPATIAL_PLAQUETTE,
    GLUEBALL_OPERATOR_SPATIAL_WILSON_LOOPS,
)
DEFAULT_SPATIAL_WILSON_LOOP_EXTENTS = ((1, 1), (1, 2), (2, 1))


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


def spatial_wilson_loop_operator(
    field: GaugeField,
    t: int,
    extents: tuple[tuple[int, int], ...] = DEFAULT_SPATIAL_WILSON_LOOP_EXTENTS,
) -> float:
    """A simple improved operator averaging small spatial Wilson loops.

    This is a baseline gauge-invariant measurement choice, not a deformation of
    the Wilson action. It averages scalar parts of 1x1, 1x2, and 2x1 spatial
    loops over each time slice.
    """

    lattice = field.lattice
    t_mod = t % lattice.shape[3]
    values: list[float] = []
    for x in range(lattice.shape[0]):
        for y in range(lattice.shape[1]):
            for z in range(lattice.shape[2]):
                site = (x, y, z, t_mod)
                for mu, nu in spatial_direction_pairs():
                    for extent_mu, extent_nu in extents:
                        values.append(wilson_loop_scalar(field, site, mu, nu, extent_mu, extent_nu))
    return float(np.mean(values))


def spatial_wilson_loop_operator_basis(
    field: GaugeField,
    t: int,
    extents: tuple[tuple[int, int], ...] = DEFAULT_SPATIAL_WILSON_LOOP_EXTENTS,
) -> dict[str, float]:
    """Return separate spatial Wilson-loop operator channels for one time slice."""

    lattice = field.lattice
    t_mod = t % lattice.shape[3]
    channels: dict[str, list[float]] = {f"spatial_loop_{extent_mu}x{extent_nu}": [] for extent_mu, extent_nu in extents}
    for x in range(lattice.shape[0]):
        for y in range(lattice.shape[1]):
            for z in range(lattice.shape[2]):
                site = (x, y, z, t_mod)
                for mu, nu in spatial_direction_pairs():
                    for extent_mu, extent_nu in extents:
                        key = f"spatial_loop_{extent_mu}x{extent_nu}"
                        channels[key].append(wilson_loop_scalar(field, site, mu, nu, extent_mu, extent_nu))
    return {key: float(np.mean(values)) for key, values in channels.items()}


def spatial_wilson_loop_basis_timeseries(
    field: GaugeField,
    extents: tuple[tuple[int, int], ...] = DEFAULT_SPATIAL_WILSON_LOOP_EXTENTS,
) -> dict[str, NDArray[np.float64]]:
    """Return one time series per spatial Wilson-loop basis channel."""

    per_time = [spatial_wilson_loop_operator_basis(field, t, extents=extents) for t in range(field.lattice.shape[3])]
    if not per_time:
        return {}
    return {
        key: np.array([channels[key] for channels in per_time], dtype=float)
        for key in per_time[0]
    }


def glueball_timeseries(
    field: GaugeField,
    operator: str = GLUEBALL_OPERATOR_SPATIAL_PLAQUETTE,
) -> NDArray[np.float64]:
    """Return ``O(t)`` for every temporal slice using a named operator."""

    if operator not in GLUEBALL_OPERATOR_MODES:
        raise ValueError(f"unknown glueball operator mode: {operator}")
    operator_fn = glueball_operator if operator == GLUEBALL_OPERATOR_SPATIAL_PLAQUETTE else spatial_wilson_loop_operator

    return np.array(
        [operator_fn(field, t) for t in range(field.lattice.shape[3])],
        dtype=float,
    )
