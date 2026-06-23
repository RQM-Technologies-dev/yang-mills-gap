"""Periodic four-dimensional lattice utilities."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import prod
from typing import Iterator


Site = tuple[int, int, int, int]


@dataclass(frozen=True)
class Lattice4D:
    """A finite 4D periodic lattice with coordinate order ``(x, y, z, t)``."""

    shape: tuple[int, int, int, int]

    def __post_init__(self) -> None:
        if len(self.shape) != 4:
            raise ValueError("Lattice4D shape must have exactly four extents")
        if any(int(length) <= 0 for length in self.shape):
            raise ValueError("all lattice extents must be positive")
        object.__setattr__(self, "shape", tuple(int(length) for length in self.shape))

    @property
    def volume(self) -> int:
        return prod(self.shape)

    @property
    def ndim(self) -> int:
        return 4

    def sites(self) -> Iterator[Site]:
        return product(*(range(length) for length in self.shape))

    def shift(self, site: Site, mu: int, step: int = 1) -> Site:
        if not 0 <= mu < 4:
            raise ValueError("direction mu must be in {0, 1, 2, 3}")
        if len(site) != 4:
            raise ValueError("site must have four coordinates")
        shifted = list(site)
        shifted[mu] = (shifted[mu] + step) % self.shape[mu]
        return tuple(shifted)  # type: ignore[return-value]
