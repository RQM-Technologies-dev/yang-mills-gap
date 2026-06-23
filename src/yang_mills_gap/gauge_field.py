"""SU(2) gauge fields stored as unit-quaternion link variables."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .lattice import Lattice4D, Site
from .quaternions import IDENTITY, inverse, multiply, normalize, random_unit_quaternion


@dataclass
class GaugeField:
    """A gauge field with links ``U[x, y, z, t, mu]`` as unit quaternions."""

    lattice: Lattice4D
    links: NDArray[np.float64]

    def __post_init__(self) -> None:
        expected_shape = self.lattice.shape + (4, 4)
        arr = np.asarray(self.links, dtype=float)
        if arr.shape != expected_shape:
            raise ValueError(f"expected link array shape {expected_shape}, got {arr.shape}")
        self.links = normalize(arr)

    @classmethod
    def cold(cls, lattice: Lattice4D) -> "GaugeField":
        links = np.zeros(lattice.shape + (4, 4), dtype=float)
        links[..., :] = IDENTITY
        return cls(lattice, links)

    @classmethod
    def random(
        cls,
        lattice: Lattice4D,
        rng: np.random.Generator | None = None,
    ) -> "GaugeField":
        links = random_unit_quaternion(rng, lattice.shape + (4,))
        return cls(lattice, links)

    def copy(self) -> "GaugeField":
        return GaugeField(self.lattice, np.array(self.links, copy=True))

    def link(self, site: Site, mu: int) -> NDArray[np.float64]:
        return self.links[site + (mu,)]

    def set_link(self, site: Site, mu: int, value: ArrayLike) -> None:
        self.links[site + (mu,)] = normalize(value)

    def transformed(self, gauges: ArrayLike) -> "GaugeField":
        """Apply local gauge transformations ``g(x)`` to all links.

        The transformed link is ``g(x) U_mu(x) g^{-1}(x + mu)``.
        """

        g = normalize(np.asarray(gauges, dtype=float))
        expected_shape = self.lattice.shape + (4,)
        if g.shape != expected_shape:
            raise ValueError(f"expected gauge array shape {expected_shape}, got {g.shape}")

        transformed = np.empty_like(self.links)
        for site in self.lattice.sites():
            for mu in range(4):
                forward_site = self.lattice.shift(site, mu)
                transformed[site + (mu,)] = multiply(
                    multiply(g[site], self.link(site, mu)),
                    inverse(g[forward_site]),
                )
        return GaugeField(self.lattice, transformed)
