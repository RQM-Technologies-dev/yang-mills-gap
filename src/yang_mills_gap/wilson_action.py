"""Wilson action for the SU(2) quaternion lattice representation."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .gauge_field import GaugeField
from .lattice import Site
from .plaquette import all_closure_defects
from .quaternions import inverse, multiply, scalar_part


def wilson_action(field: GaugeField, beta: float) -> float:
    """Return ``S = beta * sum_p (1 - scalar_part(U_p))``."""

    if beta < 0:
        raise ValueError("beta must be nonnegative")
    return float(beta * np.sum(all_closure_defects(field)))


def staple_sum(field: GaugeField, site: Site, mu: int) -> NDArray[np.float64]:
    """Return the sum of forward and backward staples touching ``U_mu(site)``.

    The scalar plaquette sum for the link is ``scalar_part(U_mu(site) * S)``,
    where ``S`` is this staple sum. The six touching plaquettes in four
    dimensions are represented once each.
    """

    if not 0 <= mu < field.lattice.ndim:
        raise ValueError("direction mu must be in {0, 1, 2, 3}")

    lattice = field.lattice
    staples = np.zeros(4, dtype=float)
    for nu in range(lattice.ndim):
        if nu == mu:
            continue

        x_plus_mu = lattice.shift(site, mu)
        x_plus_nu = lattice.shift(site, nu)
        x_minus_nu = lattice.shift(site, nu, step=-1)
        x_plus_mu_minus_nu = lattice.shift(x_minus_nu, mu)

        forward = multiply(
            multiply(field.link(x_plus_mu, nu), inverse(field.link(x_plus_nu, mu))),
            inverse(field.link(site, nu)),
        )
        backward = multiply(
            multiply(inverse(field.link(x_plus_mu_minus_nu, nu)), inverse(field.link(x_minus_nu, mu))),
            field.link(x_minus_nu, nu),
        )
        staples += forward + backward

    return staples


def local_wilson_action_contribution(
    field: GaugeField,
    site: Site,
    mu: int,
    beta: float,
    *,
    link: ArrayLike | None = None,
) -> float:
    """Return the Wilson-action contribution from plaquettes touching one link.

    Supplying ``link`` evaluates the local contribution for a proposed link
    without mutating the field. Proposed links must be explicit unit
    quaternions with shape ``(4,)``. The returned contribution is suitable for
    action-difference tests and local Metropolis proposals.
    """

    if beta < 0:
        raise ValueError("beta must be nonnegative")
    if not 0 <= mu < field.lattice.ndim:
        raise ValueError("direction mu must be in {0, 1, 2, 3}")

    if link is None:
        candidate_link = field.link(site, mu)
    else:
        candidate_link = np.asarray(link, dtype=float)
        if candidate_link.shape != (4,):
            raise ValueError("candidate link must have shape (4,)")
        if not np.isclose(np.linalg.norm(candidate_link), 1.0):
            raise ValueError("candidate link must have unit norm")
    scalar_sum = float(scalar_part(multiply(candidate_link, staple_sum(field, site, mu))))
    touching_plaquettes = 2 * (field.lattice.ndim - 1)
    return float(beta * (touching_plaquettes - scalar_sum))
